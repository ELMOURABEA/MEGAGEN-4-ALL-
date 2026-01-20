import { supabase } from '../config/supabase'

export const chatService = {
  async getMessages(agentId = null) {
    let query = supabase
      .from('chat_messages')
      .select('*')
      .order('created_at', { ascending: true })

    if (agentId) {
      query = query.eq('agent_id', agentId)
    }

    const { data, error } = await query

    if (error) throw error
    return data
  },

  async sendMessage(message) {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) throw new Error('Not authenticated')

    const { data, error } = await supabase
      .from('chat_messages')
      .insert([{ ...message, user_id: user.id }])
      .select()
      .single()

    if (error) throw error
    return data
  },

  async deleteMessage(id) {
    const { error } = await supabase
      .from('chat_messages')
      .delete()
      .eq('id', id)

    if (error) throw error
  },

  subscribeToMessages(callback) {
    const subscription = supabase
      .channel('chat_messages')
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table: 'chat_messages',
        },
        (payload) => {
          callback(payload)
        }
      )
      .subscribe()

    return subscription
  },
}
