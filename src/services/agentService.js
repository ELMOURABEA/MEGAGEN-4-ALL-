import { supabase } from '../config/supabase'

export const agentService = {
  async getAgents() {
    const { data, error } = await supabase
      .from('agents')
      .select('*')
      .order('created_at', { ascending: false })

    if (error) throw error
    return data
  },

  async createAgent(agent) {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) throw new Error('Not authenticated')

    const { data, error } = await supabase
      .from('agents')
      .insert([{ ...agent, user_id: user.id }])
      .select()
      .single()

    if (error) throw error
    return data
  },

  async updateAgent(id, updates) {
    const { data, error } = await supabase
      .from('agents')
      .update(updates)
      .eq('id', id)
      .select()
      .single()

    if (error) throw error
    return data
  },

  async deleteAgent(id) {
    const { error } = await supabase
      .from('agents')
      .delete()
      .eq('id', id)

    if (error) throw error
  },

  async getAgentActivities(limit = 5) {
    const { data, error } = await supabase
      .from('agent_activities')
      .select(`
        *,
        agents (name)
      `)
      .order('created_at', { ascending: false })
      .limit(limit)

    if (error) throw error
    return data
  },

  async createActivity(activity) {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) throw new Error('Not authenticated')

    const { data, error } = await supabase
      .from('agent_activities')
      .insert([{ ...activity, user_id: user.id }])
      .select()
      .single()

    if (error) throw error
    return data
  },
}
