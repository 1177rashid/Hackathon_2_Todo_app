# Deployment Guide

## Production Deployment

### Frontend (Vercel)
- **URL**: https://frontend-50jyge5g2-rashids-projects-d543583d.vercel.app
- **Platform**: Vercel
- **Account**: 1177rashid
- **Framework**: Next.js 16+

#### Environment Variables (Vercel)
```
NEXT_PUBLIC_API_URL=https://smrashid-my-todo-app.hf.space
```

### Backend (Hugging Face Space)
- **URL**: https://smrashid-my-todo-app.hf.space
- **Platform**: Hugging Face Spaces
- **Account**: Smrashid
- **Framework**: FastAPI (Docker)

#### Environment Variables (Hugging Face)
Required secrets to set in HF Space settings:
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=<generated-secret>
JWT_SECRET=<generated-jwt-secret>
```

Generate secrets with:
```bash
openssl rand -base64 32
```

### Database (Neon/Supabase)
Choose one of these free PostgreSQL options:

**Option 1: Neon**
1. Sign up at https://neon.tech
2. Create a database
3. Copy connection string
4. Add to HF Space as `DATABASE_URL`

**Option 2: Supabase**
1. Sign up at https://supabase.com
2. Create a project
3. Get connection string from Settings > Database
4. Add to HF Space as `DATABASE_URL`

## Deployment Commands

### Frontend (Vercel)
```bash
cd frontend
vercel --prod
```

### Backend (Hugging Face)
```bash
git clone https://huggingface.co/spaces/Smrashid/my-todo-app
cd my-todo-app
# Copy backend files
git add .
git commit -m "Update backend"
git push
```

## API Documentation

Once backend is deployed:
- **Swagger UI**: https://smrashid-my-todo-app.hf.space/docs
- **ReDoc**: https://smrashid-my-todo-app.hf.space/redoc

## Access the Application

**Live App**: https://frontend-50jyge5g2-rashids-projects-d543583d.vercel.app

1. Sign up for an account
2. Log in
3. Start creating tasks!

## Monitoring & Logs

### Vercel Logs
```bash
vercel logs frontend-50jyge5g2-rashids-projects-d543583d.vercel.app
```

### Hugging Face Logs
Check logs at: https://huggingface.co/spaces/Smrashid/my-todo-app/logs

## Update Deployment

### Frontend
```bash
cd frontend
vercel --prod
```

### Backend
```bash
cd hf-space
git pull
# Make changes
git add .
git commit -m "Update"
git push
```

## Troubleshooting

### Frontend can't connect to backend
- Check `NEXT_PUBLIC_API_URL` in Vercel settings
- Verify backend is running at https://smrashid-my-todo-app.hf.space
- Check CORS settings in backend

### Database connection errors
- Verify `DATABASE_URL` in HF Space settings
- Check database is accessible
- Run migrations: SSH into HF Space or redeploy

### Authentication issues
- Verify `JWT_SECRET` and `SECRET_KEY` are set
- Check token expiration settings
- Clear browser cookies and try again

## Security Notes

⚠️ **Important Security Steps:**
1. Never commit `.env` files or secrets to git
2. Use strong random secrets (32+ characters)
3. Rotate secrets regularly
4. Use HTTPS only (both platforms provide this)
5. Set proper CORS origins in backend

## Cost

- **Vercel**: Free tier (Hobby plan)
- **Hugging Face**: Free tier
- **Neon/Supabase**: Free tier with limitations

Monitor usage to stay within free tier limits.

---

**Deployed by**: 1177rashid
**Last Updated**: 2026-02-06
