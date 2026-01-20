import { supabase } from '../config/supabase'

export const octogenService = {
  async getTentacles() {
    const { data, error } = await supabase
      .from('ai_agents')
      .select('*')
      .order('name', { ascending: true })

    if (error) throw error
    return data
  },

  async getSubscription() {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) throw new Error('Not authenticated')

    const { data, error } = await supabase
      .from('subscriptions')
      .select('*')
      .eq('user_id', user.id)
      .maybeSingle()

    if (error) throw error
    return data
  },

  async createOrchestrationTask(task) {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) throw new Error('Not authenticated')

    const { data, error } = await supabase
      .from('orchestration_tasks')
      .insert([{ ...task, user_id: user.id }])
      .select()
      .single()

    if (error) throw error
    return data
  },

  async getOrchestrationTasks(limit = 10) {
    const { data, error } = await supabase
      .from('orchestration_tasks')
      .select('*')
      .order('created_at', { ascending: false })
      .limit(limit)

    if (error) throw error
    return data
  },

  async createDreamAchievement(dream) {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) throw new Error('Not authenticated')

    const { data, error } = await supabase
      .from('dream_achievements')
      .insert([{ ...dream, user_id: user.id }])
      .select()
      .single()

    if (error) throw error
    return data
  },

  async getDreamAchievements() {
    const { data, error } = await supabase
      .from('dream_achievements')
      .select('*')
      .order('created_at', { ascending: false })

    if (error) throw error
    return data
  },

  async updateDreamAchievement(id, updates) {
    const { data, error } = await supabase
      .from('dream_achievements')
      .update(updates)
      .eq('id', id)
      .select()
      .single()

    if (error) throw error
    return data
  },

  async createResearchOperation(research) {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) throw new Error('Not authenticated')

    const { data, error } = await supabase
      .from('research_operations')
      .insert([{ ...research, user_id: user.id }])
      .select()
      .single()

    if (error) throw error
    return data
  },

  async getResearchOperations(limit = 10) {
    const { data, error } = await supabase
      .from('research_operations')
      .select('*')
      .order('created_at', { ascending: false })
      .limit(limit)

    if (error) throw error
    return data
  },

  async getUsageStats() {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) throw new Error('Not authenticated')

    const subscription = await this.getSubscription()

    const { data: orchestrationCount } = await supabase
      .from('orchestration_tasks')
      .select('id', { count: 'exact', head: true })
      .eq('user_id', user.id)

    const { data: dreamCount } = await supabase
      .from('dream_achievements')
      .select('id', { count: 'exact', head: true })
      .eq('user_id', user.id)

    const { data: researchCount } = await supabase
      .from('research_operations')
      .select('id', { count: 'exact', head: true })
      .eq('user_id', user.id)

    return {
      subscription: subscription || {
        tier: 'free',
        queries_today: 0,
        research_today: 0,
      },
      totalTasks: orchestrationCount || 0,
      totalDreams: dreamCount || 0,
      totalResearch: researchCount || 0,
    }
  },

  async updateSubscription(tier) {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) throw new Error('Not authenticated')

    const tierConfig = {
      free: { price: 0, queries_limit: 10, research_limit: 5 },
      pro: { price: 9.99, queries_limit: -1, research_limit: -1 },
      enterprise: { price: 29.99, queries_limit: -1, research_limit: -1 },
    }

    const config = tierConfig[tier] || tierConfig.free

    const { data: existing } = await supabase
      .from('subscriptions')
      .select('id')
      .eq('user_id', user.id)
      .maybeSingle()

    if (existing) {
      const { data, error } = await supabase
        .from('subscriptions')
        .update({ tier, ...config })
        .eq('user_id', user.id)
        .select()
        .single()

      if (error) throw error
      return data
    } else {
      const { data, error } = await supabase
        .from('subscriptions')
        .insert([{ user_id: user.id, tier, ...config }])
        .select()
        .single()

      if (error) throw error
      return data
    }
  },
}
