import { NextRequest, NextResponse } from 'next/server'
import { auth } from '@/lib/auth-server'
import jwt from 'jsonwebtoken'

/**
 * Generate JWT token for authenticated user
 *
 * This endpoint creates a JWT token that can be sent to the FastAPI backend.
 * The token is signed with the same BETTER_AUTH_SECRET used by both
 * Better Auth and the FastAPI backend.
 */
export async function GET(request: NextRequest) {
  try {
    // Get current session from Better Auth
    const session = await auth.api.getSession({ headers: request.headers })

    if (!session?.user) {
      return NextResponse.json(
        { error: 'Not authenticated' },
        { status: 401 }
      )
    }

    // Get secret from environment
    const secret = process.env.BETTER_AUTH_SECRET
    if (!secret) {
      console.error('BETTER_AUTH_SECRET not configured')
      return NextResponse.json(
        { error: 'Server configuration error' },
        { status: 500 }
      )
    }

    // Create JWT token with user ID
    const token = jwt.sign(
      {
        sub: session.user.id,  // User ID in 'sub' claim (standard JWT claim)
        iat: Math.floor(Date.now() / 1000),
        exp: Math.floor(Date.now() / 1000) + (7 * 24 * 60 * 60) // 7 days
      },
      secret,
      { algorithm: 'HS256' }
    )

    return NextResponse.json({
      token,
      user: {
        id: session.user.id,
        email: session.user.email,
        name: session.user.name
      }
    })
  } catch (error) {
    console.error('Token generation error:', error)
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Failed to generate token' },
      { status: 500 }
    )
  }
}
