import { Pool } from "pg"
import { config } from "dotenv"
import { resolve } from "path"

// Load environment variables from .env file
config({ path: resolve(__dirname, "../.env") })

const databaseUrl = process.env.DATABASE_URL

if (!databaseUrl) {
  console.error('❌ DATABASE_URL environment variable is not set')
  process.exit(1)
}

async function migrate() {
  const pool = new Pool({
    connectionString: databaseUrl,
    ssl: databaseUrl!.includes('sslmode=require') ? { rejectUnauthorized: false } : undefined
  })

  try {
    console.log('🔄 Starting Better Auth database migration...')

    // Drop existing tables to recreate with correct schema
    await pool.query(`
      DROP TABLE IF EXISTS "verification" CASCADE;
      DROP TABLE IF EXISTS "session" CASCADE;
      DROP TABLE IF EXISTS "account" CASCADE;
      DROP TABLE IF EXISTS "user" CASCADE;
    `)

    // Better Auth tables schema (complete)
    await pool.query(`
      -- Create user table
      CREATE TABLE "user" (
        "id" TEXT PRIMARY KEY,
        "email" TEXT NOT NULL UNIQUE,
        "emailVerified" BOOLEAN NOT NULL DEFAULT false,
        "name" TEXT,
        "image" TEXT,
        "createdAt" TIMESTAMP NOT NULL DEFAULT NOW(),
        "updatedAt" TIMESTAMP NOT NULL DEFAULT NOW()
      );

      -- Create account table
      CREATE TABLE "account" (
        "id" TEXT PRIMARY KEY,
        "userId" TEXT NOT NULL REFERENCES "user"("id") ON DELETE CASCADE,
        "accountId" TEXT NOT NULL,
        "providerId" TEXT NOT NULL,
        "accessToken" TEXT,
        "refreshToken" TEXT,
        "expiresAt" TIMESTAMP,
        "password" TEXT,
        "createdAt" TIMESTAMP NOT NULL DEFAULT NOW(),
        "updatedAt" TIMESTAMP NOT NULL DEFAULT NOW()
      );

      -- Create session table with token column
      CREATE TABLE "session" (
        "id" TEXT PRIMARY KEY,
        "userId" TEXT NOT NULL REFERENCES "user"("id") ON DELETE CASCADE,
        "token" TEXT NOT NULL UNIQUE,
        "expiresAt" TIMESTAMP NOT NULL,
        "ipAddress" TEXT,
        "userAgent" TEXT,
        "createdAt" TIMESTAMP NOT NULL DEFAULT NOW(),
        "updatedAt" TIMESTAMP NOT NULL DEFAULT NOW()
      );

      -- Create verification table
      CREATE TABLE "verification" (
        "id" TEXT PRIMARY KEY,
        "identifier" TEXT NOT NULL,
        "value" TEXT NOT NULL,
        "expiresAt" TIMESTAMP NOT NULL,
        "createdAt" TIMESTAMP NOT NULL DEFAULT NOW(),
        "updatedAt" TIMESTAMP NOT NULL DEFAULT NOW()
      );

      -- Create indexes
      CREATE INDEX "idx_account_userId" ON "account"("userId");
      CREATE INDEX "idx_session_userId" ON "session"("userId");
      CREATE INDEX "idx_session_token" ON "session"("token");
      CREATE INDEX "idx_verification_identifier" ON "verification"("identifier");
    `)

    console.log('✅ Migration completed successfully!')
    console.log('   - user table created')
    console.log('   - account table created')
    console.log('   - session table created')
    console.log('   - verification table created')

    await pool.end()
    process.exit(0)
  } catch (error) {
    console.error('❌ Migration failed:', error)
    await pool.end()
    process.exit(1)
  }
}

migrate()
