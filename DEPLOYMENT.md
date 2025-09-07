# Deployment Guide

This guide covers deploying the Soil Carbon API to various cloud platforms.

## 🚀 Railway (Recommended)

### Prerequisites
- GitHub repository with your code
- Railway account (free at https://railway.app)

### Steps
1. **Sign up for Railway**
   - Go to https://railway.app
   - Sign up with your GitHub account

2. **Deploy from GitHub**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `soil-carbon-api` repository
   - Railway will automatically detect it's a Python app

3. **Configure Environment**
   - Railway will automatically install dependencies from `requirements.txt`
   - The app will start using the `railway.json` configuration

4. **Access Your API**
   - Railway provides a public URL (e.g., `https://your-app-name.railway.app`)
   - Your API will be available at `https://your-app-name.railway.app/soil_carbon`

### Testing Deployment
```bash
curl -X POST "https://your-app-name.railway.app/soil_carbon" \
  -H "Content-Type: application/json" \
  -d '{"latitude": 42.3601, "longitude": -71.0589, "max_distance_km": 10.0}'
```

## 🌐 Render

### Steps
1. **Sign up for Render**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create New Web Service**
   - Connect your GitHub repository
   - Choose "Web Service"
   - Select your repository

3. **Configure Build**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy your app

## 🐳 Fly.io

### Prerequisites
- Install Fly CLI: https://fly.io/docs/hands-on/install-flyctl/

### Steps
1. **Login to Fly**
   ```bash
   fly auth login
   ```

2. **Initialize Fly App**
   ```bash
   fly launch
   ```

3. **Deploy**
   ```bash
   fly deploy
   ```

## ☁️ Vercel (Serverless)

### Steps
1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   vercel
   ```

3. **Configure for FastAPI**
   - Create `vercel.json`:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "main.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "main.py"
       }
     ]
   }
   ```

## 🔧 Environment Variables

Some platforms may require environment variables:

- `PORT`: Automatically set by most platforms
- `PYTHONPATH`: Set to `/app` if needed

## 📊 Monitoring

After deployment, monitor your app:
- Check logs for any errors
- Monitor response times
- Set up health checks

## 🔄 Continuous Deployment

All platforms support automatic deployments:
- Push to `main` branch triggers automatic deployment
- Monitor deployment status in platform dashboard

## 🆘 Troubleshooting

### Common Issues
1. **Port binding errors**: Ensure your app uses `$PORT` environment variable
2. **Dependency issues**: Check `requirements.txt` has all needed packages
3. **Memory issues**: Some platforms have memory limits

### Debug Commands
```bash
# Check logs
railway logs

# Check app status
railway status

# Connect to app shell
railway shell
```

## 📈 Scaling

- **Railway**: Upgrade to paid plan for more resources
- **Render**: Upgrade to paid plan for always-on instances
- **Fly.io**: Scale horizontally with `fly scale count 2`
- **Vercel**: Automatic scaling with Pro plan
