import { supabase } from '../config/supabase'

export const userService = {
  async getProfile() {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) throw new Error('Not authenticated')

    const { data, error } = await supabase
      .from('user_profiles')
      .select('*')
      .eq('id', user.id)
      .maybeSingle()

    if (error) throw error
    return data
  },

  async createProfile(email) {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) throw new Error('Not authenticated')

    const { data, error } = await supabase
      .from('user_profiles')
      .insert([{
        id: user.id,
        email: email,
        subscription_tier: 'free',
      }])
      .select()
      .single()

    if (error) throw error
    return data
  },

  async updateProfile(updates) {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) throw new Error('Not authenticated')

    const { data, error } = await supabase
      .from('user_profiles')
      .update(updates)
      .eq('id', user.id)
      .select()
      .single()

    if (error) throw error
    return data
  },

  async getOrCreateProfile(email) {
    let profile = await this.getProfile()

    if (!profile) {
      profile = await this.createProfile(email)
    }

    return profile
  },
}
