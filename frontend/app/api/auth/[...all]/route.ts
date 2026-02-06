import { auth } from "@/lib/auth-server"
import { NextResponse } from 'next/server'

// CORS headers for cross-origin requests
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  'Access-Control-Allow-Credentials': 'true',
}

export async function OPTIONS() {
  return NextResponse.json({}, { headers: corsHeaders })
}

export async function GET(request: Request) {
  try {
    const response = await auth.handler(request)
    // Add CORS headers to the response
    Object.entries(corsHeaders).forEach(([key, value]) => {
      response.headers.set(key, value)
    })
    return response
  } catch (error) {
    console.error('Auth GET error:', error)
    return NextResponse.json({
      error: error instanceof Error ? error.message : 'Authentication error',
      details: error instanceof Error ? error.stack : undefined
    }, { status: 500, headers: corsHeaders })
  }
}

export async function POST(request: Request) {
  try {
    const response = await auth.handler(request)
    // Add CORS headers to the response
    Object.entries(corsHeaders).forEach(([key, value]) => {
      response.headers.set(key, value)
    })
    return response
  } catch (error) {
    console.error('Auth POST error:', error)
    return NextResponse.json({
      error: error instanceof Error ? error.message : 'Authentication error',
      details: error instanceof Error ? error.stack : undefined
    }, { status: 500, headers: corsHeaders })
  }
}
