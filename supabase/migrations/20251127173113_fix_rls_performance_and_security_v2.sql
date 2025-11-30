/*
  # Fix RLS Performance and Security Issues

  ## Changes
  1. Optimize all RLS policies by wrapping auth.uid() in SELECT subqueries
  2. Fix function search path security issue
  
  ## Performance Impact
  - Prevents re-evaluation of auth.uid() for each row
  - Significantly improves query performance at scale
  
  ## Security Impact
  - Fixes mutable search_path security vulnerability
*/

-- First, drop all existing policies that need to be recreated
DROP POLICY IF EXISTS "Users can view own profile" ON user_profiles;
DROP POLICY IF EXISTS "Users can insert own profile" ON user_profiles;
DROP POLICY IF EXISTS "Users can update own profile" ON user_profiles;

DROP POLICY IF EXISTS "Users can view own agents" ON agents;
DROP POLICY IF EXISTS "Users can insert own agents" ON agents;
DROP POLICY IF EXISTS "Users can update own agents" ON agents;
DROP POLICY IF EXISTS "Users can delete own agents" ON agents;

DROP POLICY IF EXISTS "Users can view own messages" ON chat_messages;
DROP POLICY IF EXISTS "Users can insert own messages" ON chat_messages;
DROP POLICY IF EXISTS "Users can delete own messages" ON chat_messages;

DROP POLICY IF EXISTS "Users can view own activities" ON agent_activities;
DROP POLICY IF EXISTS "Users can insert own activities" ON agent_activities;
DROP POLICY IF EXISTS "Users can delete own activities" ON agent_activities;

DROP POLICY IF EXISTS "Users can view own tasks" ON orchestration_tasks;
DROP POLICY IF EXISTS "Users can insert own tasks" ON orchestration_tasks;
DROP POLICY IF EXISTS "Users can update own tasks" ON orchestration_tasks;

DROP POLICY IF EXISTS "Users can view own subscription" ON subscriptions;
DROP POLICY IF EXISTS "Users can insert own subscription" ON subscriptions;
DROP POLICY IF EXISTS "Users can update own subscription" ON subscriptions;

DROP POLICY IF EXISTS "Users can view own usage logs" ON usage_logs;
DROP POLICY IF EXISTS "Users can insert own usage logs" ON usage_logs;

DROP POLICY IF EXISTS "Users can view own dreams" ON dream_achievements;
DROP POLICY IF EXISTS "Users can insert own dreams" ON dream_achievements;
DROP POLICY IF EXISTS "Users can update own dreams" ON dream_achievements;

DROP POLICY IF EXISTS "Users can view own research" ON research_operations;
DROP POLICY IF EXISTS "Users can insert own research" ON research_operations;
DROP POLICY IF EXISTS "Users can update own research" ON research_operations;

-- Recreate optimized policies for user_profiles
CREATE POLICY "Users can view own profile"
  ON user_profiles FOR SELECT
  TO authenticated
  USING ((select auth.uid()) = id);

CREATE POLICY "Users can insert own profile"
  ON user_profiles FOR INSERT
  TO authenticated
  WITH CHECK ((select auth.uid()) = id);

CREATE POLICY "Users can update own profile"
  ON user_profiles FOR UPDATE
  TO authenticated
  USING ((select auth.uid()) = id)
  WITH CHECK ((select auth.uid()) = id);

-- Recreate optimized policies for agents
CREATE POLICY "Users can view own agents"
  ON agents FOR SELECT
  TO authenticated
  USING ((select auth.uid()) = user_id);

CREATE POLICY "Users can insert own agents"
  ON agents FOR INSERT
  TO authenticated
  WITH CHECK ((select auth.uid()) = user_id);

CREATE POLICY "Users can update own agents"
  ON agents FOR UPDATE
  TO authenticated
  USING ((select auth.uid()) = user_id)
  WITH CHECK ((select auth.uid()) = user_id);

CREATE POLICY "Users can delete own agents"
  ON agents FOR DELETE
  TO authenticated
  USING ((select auth.uid()) = user_id);

-- Recreate optimized policies for chat_messages
CREATE POLICY "Users can view own messages"
  ON chat_messages FOR SELECT
  TO authenticated
  USING ((select auth.uid()) = user_id);

CREATE POLICY "Users can insert own messages"
  ON chat_messages FOR INSERT
  TO authenticated
  WITH CHECK ((select auth.uid()) = user_id);

CREATE POLICY "Users can delete own messages"
  ON chat_messages FOR DELETE
  TO authenticated
  USING ((select auth.uid()) = user_id);

-- Recreate optimized policies for agent_activities
CREATE POLICY "Users can view own activities"
  ON agent_activities FOR SELECT
  TO authenticated
  USING ((select auth.uid()) = user_id);

CREATE POLICY "Users can insert own activities"
  ON agent_activities FOR INSERT
  TO authenticated
  WITH CHECK ((select auth.uid()) = user_id);

CREATE POLICY "Users can delete own activities"
  ON agent_activities FOR DELETE
  TO authenticated
  USING ((select auth.uid()) = user_id);

-- Recreate optimized policies for orchestration_tasks
CREATE POLICY "Users can view own tasks"
  ON orchestration_tasks FOR SELECT
  TO authenticated
  USING ((select auth.uid()) = user_id);

CREATE POLICY "Users can insert own tasks"
  ON orchestration_tasks FOR INSERT
  TO authenticated
  WITH CHECK ((select auth.uid()) = user_id);

CREATE POLICY "Users can update own tasks"
  ON orchestration_tasks FOR UPDATE
  TO authenticated
  USING ((select auth.uid()) = user_id)
  WITH CHECK ((select auth.uid()) = user_id);

-- Recreate optimized policies for subscriptions
CREATE POLICY "Users can view own subscription"
  ON subscriptions FOR SELECT
  TO authenticated
  USING ((select auth.uid()) = user_id);

CREATE POLICY "Users can insert own subscription"
  ON subscriptions FOR INSERT
  TO authenticated
  WITH CHECK ((select auth.uid()) = user_id);

CREATE POLICY "Users can update own subscription"
  ON subscriptions FOR UPDATE
  TO authenticated
  USING ((select auth.uid()) = user_id)
  WITH CHECK ((select auth.uid()) = user_id);

-- Recreate optimized policies for usage_logs
CREATE POLICY "Users can view own usage logs"
  ON usage_logs FOR SELECT
  TO authenticated
  USING ((select auth.uid()) = user_id);

CREATE POLICY "Users can insert own usage logs"
  ON usage_logs FOR INSERT
  TO authenticated
  WITH CHECK ((select auth.uid()) = user_id);

-- Recreate optimized policies for dream_achievements
CREATE POLICY "Users can view own dreams"
  ON dream_achievements FOR SELECT
  TO authenticated
  USING ((select auth.uid()) = user_id);

CREATE POLICY "Users can insert own dreams"
  ON dream_achievements FOR INSERT
  TO authenticated
  WITH CHECK ((select auth.uid()) = user_id);

CREATE POLICY "Users can update own dreams"
  ON dream_achievements FOR UPDATE
  TO authenticated
  USING ((select auth.uid()) = user_id)
  WITH CHECK ((select auth.uid()) = user_id);

-- Recreate optimized policies for research_operations
CREATE POLICY "Users can view own research"
  ON research_operations FOR SELECT
  TO authenticated
  USING ((select auth.uid()) = user_id);

CREATE POLICY "Users can insert own research"
  ON research_operations FOR INSERT
  TO authenticated
  WITH CHECK ((select auth.uid()) = user_id);

CREATE POLICY "Users can update own research"
  ON research_operations FOR UPDATE
  TO authenticated
  USING ((select auth.uid()) = user_id)
  WITH CHECK ((select auth.uid()) = user_id);

-- Fix function search path security issue using CASCADE
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$;

-- Recreate all triggers that were dropped
CREATE TRIGGER update_user_profiles_updated_at
  BEFORE UPDATE ON user_profiles
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agents_updated_at
  BEFORE UPDATE ON agents
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ai_agents_updated_at
  BEFORE UPDATE ON ai_agents
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subscriptions_updated_at
  BEFORE UPDATE ON subscriptions
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_dream_achievements_updated_at
  BEFORE UPDATE ON dream_achievements
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
