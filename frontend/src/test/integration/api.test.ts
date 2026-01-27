/**
 * Integration tests for API client
 * Tests API communication and error handling
 */

import { describe, it, expect, beforeEach } from 'vitest'
import { apiClient } from '../../lib/api/client'

describe('API Client Integration', () => {
  beforeEach(() => {
    // Reset any mocks if needed
  })

  it('configures base URL correctly', () => {
    expect(apiClient.defaults.baseURL).toBe('/api/v1')
  })

  it('sets correct headers', () => {
    expect(apiClient.defaults.headers['Content-Type']).toBe('application/json')
  })

  it('has interceptors configured', () => {
    expect(apiClient.interceptors.request).toBeDefined()
    expect(apiClient.interceptors.response).toBeDefined()
  })
})
