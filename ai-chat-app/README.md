# AI Chat Interface

A modern chat interface built with Next.js, TypeScript, and Tailwind CSS that integrates with OpenAI's API to provide AI-powered conversations.

## Features

- 🤖 **Multiple AI Models**: Support for GPT-3.5 Turbo, GPT-4, and other OpenAI models
- 💬 **Real-time Chat**: Smooth, responsive chat interface with typing indicators
- 🎨 **Modern UI**: Clean, professional design with Tailwind CSS
- 📱 **Responsive**: Works on desktop and mobile devices
- ⚡ **Fast**: Built with Next.js 14 and optimized for performance

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Set Up Environment Variables

Create a `.env.local` file in the root directory and add your OpenAI API key:

```bash
# OpenAI API Key
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Deployment

### Deploy to Vercel

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Add your `OPENAI_API_KEY` environment variable in Vercel settings
4. Deploy!

### Manual Deployment

```bash
npm run build
npm start
```

## Usage

1. Select your preferred AI model from the dropdown in the top-right corner
2. Type your message in the input field
3. Press Enter or click the Send button
4. The AI will respond with helpful, contextual information

## AIE7 Assignment Integration

This chat interface is designed to work with the AIE7 assignment requirements:

### Vibe Check Questions

You can test the following questions to evaluate the system:

1. **Object-Oriented Programming**: "Explain the concept of object-oriented programming in simple terms to a complete beginner."
2. **Text Summarization**: "Read the following paragraph and provide a concise summary of the key points..."
3. **Creative Writing**: "Write a short, imaginative story (100–150 words) about a robot finding friendship in an unexpected place."
4. **Mathematical Reasoning**: "If a store sells apples in packs of 4 and oranges in packs of 3, how many packs of each do I need to buy to get exactly 12 apples and 9 oranges?"
5. **Tone Conversion**: "Rewrite the following paragraph in a professional, formal tone..."

### Model Selection

The interface supports multiple OpenAI models to help you test different capabilities:
- **GPT-3.5 Turbo**: Fast and cost-effective for general tasks
- **GPT-4**: More capable for complex reasoning and creative tasks
- **GPT-3.5 Turbo 16K**: For longer conversations
- **GPT-4o**: Latest model with enhanced capabilities

## Customization

You can customize the chat interface by modifying:
- `src/components/ChatInterface.tsx`: Main chat component
- `src/app/api/chat/route.ts`: API endpoint for OpenAI integration
- `tailwind.config.js`: Styling and theme customization

## Technologies Used

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **OpenAI API**: AI model integration
- **Lucide React**: Beautiful icons
- **Vercel**: Deployment platform

## License

MIT License - feel free to use this project for your AIE7 assignment and beyond!
