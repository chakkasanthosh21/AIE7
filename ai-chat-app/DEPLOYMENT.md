# Deployment Guide for AIE7 Assignment

This guide will help you deploy your AI Chat Interface to Vercel for the AIE7 assignment.

## Prerequisites

1. **GitHub Account**: You'll need a GitHub account to host your code
2. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
3. **OpenAI API Key**: Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)

## Step 1: Prepare Your Repository

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit: AI Chat Interface"
   ```

2. **Create GitHub Repository**:
   - Go to [GitHub](https://github.com) and create a new repository
   - Name it something like `ai-chat-interface` or `aie7-challenge`
   - Make it public or private (your choice)

3. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

## Step 2: Deploy to Vercel

1. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com) and sign in
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will automatically detect it's a Next.js project

2. **Configure Environment Variables**:
   - In the Vercel project settings, go to "Environment Variables"
   - Add a new variable:
     - **Name**: `OPENAI_API_KEY`
     - **Value**: Your OpenAI API key
     - **Environment**: Production, Preview, and Development
   - Click "Save"

3. **Deploy**:
   - Click "Deploy" in Vercel
   - Wait for the build to complete
   - Your app will be live at `https://your-project-name.vercel.app`

## Step 3: Test Your Deployment

1. **Visit your deployed URL**
2. **Test the vibe check questions**:
   - Explain object-oriented programming to a beginner
   - Ask for a story about a robot finding friendship
   - Test mathematical reasoning with the apples/oranges problem
   - Try text summarization
   - Test tone conversion

3. **Take Screenshots** for your assignment submission

## Step 4: Assignment Submission

For the AIE7 assignment, you'll need to provide:

1. **GitHub Repository URL**: `https://github.com/YOUR_USERNAME/YOUR_REPO_NAME`
2. **Vercel Deployment URL**: `https://your-project-name.vercel.app`
3. **Screenshots** of your vibe check results

## Troubleshooting

### Common Issues

1. **Environment Variable Not Set**:
   - Make sure `OPENAI_API_KEY` is set in Vercel environment variables
   - Redeploy after adding the variable

2. **Build Errors**:
   - Check the build logs in Vercel
   - Ensure all dependencies are in `package.json`

3. **API Errors**:
   - Verify your OpenAI API key is valid
   - Check your OpenAI account has credits

### Getting Help

- Check Vercel's [deployment documentation](https://vercel.com/docs)
- Review the [Next.js deployment guide](https://nextjs.org/docs/app/building-your-application/deploying)
- Contact your instructor if you encounter issues

## Security Notes

- Never commit your `.env.local` file to Git
- Use environment variables in Vercel for sensitive data
- Consider setting up API key restrictions in OpenAI

## Next Steps

After deployment:

1. **Test thoroughly** with the vibe check questions
2. **Document your findings** in your assignment submission
3. **Consider improvements** based on the vibe check results
4. **Iterate and redeploy** if needed

Good luck with your AIE7 assignment! 🚀 