import { Metadata } from 'next'
import Image from 'next/image'

export const metadata: Metadata = {
  title: 'Features - Intrix',
  description: 'Discover the powerful features of Intrix that help you analyze and understand your data.',
}

const features = [
  {
    title: 'Advanced Data Analysis',
    description: 'Leverage cutting-edge AI to analyze your data with precision and depth, uncovering valuable insights and patterns.',
    icon: '📊',
  },
  {
    title: 'Real-time Processing',
    description: 'Get instant results with our high-performance processing engine that handles data in real-time.',
    icon: '⚡',
  },
  {
    title: 'Customizable Reports',
    description: 'Generate detailed, customizable reports that present your data in clear, actionable formats.',
    icon: '📈',
  },
  {
    title: 'Secure Data Handling',
    description: 'Your data security is our top priority with enterprise-grade encryption and privacy controls.',
    icon: '🔒',
  },
  {
    title: 'Intuitive Dashboard',
    description: 'Navigate through your data with our user-friendly interface designed for optimal user experience.',
    icon: '🎯',
  },
  {
    title: 'API Integration',
    description: 'Seamlessly integrate with your existing systems through our comprehensive API suite.',
    icon: '🔌',
  },
]

export default function FeaturesPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl">
            Powerful Features
          </h1>
          <p className="mt-4 text-xl text-gray-600 max-w-3xl mx-auto">
            Discover how Intrix can transform your data analysis workflow with our comprehensive suite of features.
          </p>
        </div>

        <div className="mt-20 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((feature, index) => (
            <div
              key={index}
              className="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition-shadow duration-300"
            >
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>

        <div className="mt-20 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Ready to Get Started?
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Join thousands of users who are already transforming their data analysis with Intrix.
          </p>
          <a
            href="/pricing"
            className="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors duration-300"
          >
            View Pricing Plans
          </a>
        </div>
      </div>
    </div>
  )
} 