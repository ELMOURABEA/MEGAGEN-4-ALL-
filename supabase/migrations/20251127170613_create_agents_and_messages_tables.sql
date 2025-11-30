/*
  # Create MEGAGENT Core Database Schema

  ## Overview
  This migration creates the foundational database schema for the MEGAGENT application,
  supporting both web and mobile platforms with real-time synchronization.

  ## New Tables

  ### `agents`
  Stores information about AI agents in the system.
  - `id` (uuid, primary key) - Unique identifier for each agent
  - `user_id` (uuid, foreign key to auth.users) - Owner of the agent
  - `name` (text) - Agent name
  - `type` (text) - Agent type (Research, Development, Analytics, Writing, Communication)
  - `status` (text) - Current status (active, idle, offline)
  - `tasks_completed` (integer) - Number of completed tasks
  - `success_rate` (integer) - Success rate percentage
  - `created_at` (timestamptz) - Creation timestamp
  - `updated_at` (timestamptz) - Last update timestamp

  ### `chat_messages`
  Stores chat messages between users and AI agents.
  - `id` (uuid, primary key) - Unique message identifier
  - `user_id` (uuid, foreign key to auth.users) - Message author
  - `agent_id` (uuid, foreign key to agents) - Associated agent (nullable)
  - `role` (text) - Message role (user, assistant)
  - `content` (text) - Message content
  - `created_at` (timestamptz) - Message timestamp

  ### `agent_activities`
  Tracks agent activities for the dashboard.
  - `id` (uuid, primary key) - Unique activity identifier
  - `agent_id` (uuid, foreign key to agents) - Associated agent
  - `user_id` (uuid, foreign key to auth.users) - Activity owner
  - `task` (text) - Task description
  - `status` (text) - Activity status (success, warning, error)
  - `created_at` (timestamptz) - Activity timestamp

  ### `user_profiles`
  Extended user profile information.
  - `id` (uuid, primary key, foreign key to auth.users) - User identifier
  - `email` (text) - User email
  - `subscription_tier` (text) - Subscription level (free, pro, enterprise)
  - `created_at` (timestamptz) - Profile creation timestamp
  - `updated_at` (timestamptz) - Last update timestamp

  ## Security
  
  All tables have Row Level Security (RLS) enabled with policies ensuring:
  - Users can only access their own data
  - Authenticated users required for all operations
  - Strict ownership checks on all queries

  ## Important Notes
  
  - All foreign keys use CASCADE on delete for data integrity
  - Timestamps use timezone-aware types for global compatibility
  - Default values provided for better data consistency
  - Indexes added on foreign keys for query performance
*/

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create user_profiles table
CREATE TABLE IF NOT EXISTS user_profiles (
  id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email text NOT NULL,
  subscription_tier text DEFAULT 'free' NOT NULL,
  created_at timestamptz DEFAULT now() NOT NULL,
  updated_at timestamptz DEFAULT now() NOT NULL
);

-- Create agents table
CREATE TABLE IF NOT EXISTS agents (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  name text NOT NULL,
  type text NOT NULL,
  status text DEFAULT 'idle' NOT NULL,
  tasks_completed integer DEFAULT 0 NOT NULL,
  success_rate integer DEFAULT 0 NOT NULL,
  created_at timestamptz DEFAULT now() NOT NULL,
  updated_at timestamptz DEFAULT now() NOT NULL
);

-- Create chat_messages table
CREATE TABLE IF NOT EXISTS chat_messages (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  agent_id uuid REFERENCES agents(id) ON DELETE SET NULL,
  role text NOT NULL,
  content text NOT NULL,
  created_at timestamptz DEFAULT now() NOT NULL
);

-- Create agent_activities table
CREATE TABLE IF NOT EXISTS agent_activities (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  agent_id uuid REFERENCES agents(id) ON DELETE CASCADE NOT NULL,
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  task text NOT NULL,
  status text DEFAULT 'success' NOT NULL,
  created_at timestamptz DEFAULT now() NOT NULL
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_agents_user_id ON agents(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_user_id ON chat_messages(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_agent_id ON chat_messages(agent_id);
CREATE INDEX IF NOT EXISTS idx_agent_activities_user_id ON agent_activities(user_id);
CREATE INDEX IF NOT EXISTS idx_agent_activities_agent_id ON agent_activities(agent_id);

-- Enable Row Level Security
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_activities ENABLE ROW LEVEL SECURITY;

-- RLS Policies for user_profiles
CREATE POLICY "Users can view own profile"
  ON user_profiles FOR SELECT
  TO authenticated
  USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile"
  ON user_profiles FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON user_profiles FOR UPDATE
  TO authenticated
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

-- RLS Policies for agents
CREATE POLICY "Users can view own agents"
  ON agents FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own agents"
  ON agents FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own agents"
  ON agents FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own agents"
  ON agents FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id);

-- RLS Policies for chat_messages
CREATE POLICY "Users can view own messages"
  ON chat_messages FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own messages"
  ON chat_messages FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own messages"
  ON chat_messages FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id);

-- RLS Policies for agent_activities
CREATE POLICY "Users can view own activities"
  ON agent_activities FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own activities"
  ON agent_activities FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own activities"
  ON agent_activities FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id);

-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers to update updated_at
CREATE TRIGGER update_user_profiles_updated_at
  BEFORE UPDATE ON user_profiles
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agents_updated_at
  BEFORE UPDATE ON agents
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
