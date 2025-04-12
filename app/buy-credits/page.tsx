'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface CreditPackage {
  id: string;
  credits: number;
  price: number;
  description: string;
}

const creditPackages: CreditPackage[] = [
  {
    id: 'price_500_credits',
    credits: 500,
    price: 5,
    description: 'Perfect for small projects',
  },
  {
    id: 'price_1000_credits',
    credits: 1000,
    price: 9,
    description: 'Best value for regular users',
  },
  {
    id: 'price_2000_credits',
    credits: 2000,
    price: 15,
    description: 'Ideal for power users',
  },
];

export default function BuyCreditsPage() {
  const router = useRouter();
  const [selectedPackage, setSelectedPackage] = useState<CreditPackage | null>(null);
  const [userCredits, setUserCredits] = useState<number>(0);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // TODO: Fetch user's current credits from API
    fetchUserCredits();
  }, []);

  const fetchUserCredits = async () => {
    try {
      const response = await fetch('/api/credits/balance');
      const data = await response.json();
      setUserCredits(data.balance);
    } catch (error) {
      console.error('Error fetching credits:', error);
    }
  };

  const handlePackageSelect = (pkg: CreditPackage) => {
    setSelectedPackage(pkg);
  };

  const handleCheckout = async () => {
    if (!selectedPackage) return;

    setIsLoading(true);
    try {
      const response = await fetch('/api/payment/create-checkout-session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          price_id: selectedPackage.id,
          user_id: 'current_user_id', // TODO: Get actual user ID
        }),
      });

      const { url } = await response.json();
      window.location.href = url;
    } catch (error) {
      console.error('Error creating checkout session:', error);
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-3xl font-bold text-gray-900">Buy Credits</h1>
          <p className="mt-4 text-lg text-gray-600">
            Current balance: <span className="font-semibold">{userCredits} credits</span>
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {creditPackages.map((pkg) => (
            <div
              key={pkg.id}
              className={`bg-white rounded-lg shadow-lg overflow-hidden ${
                selectedPackage?.id === pkg.id
                  ? 'ring-2 ring-blue-500'
                  : 'hover:shadow-xl transition-shadow'
              }`}
            >
              <div className="p-6">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">
                  {pkg.credits} Credits
                </h3>
                <p className="text-3xl font-bold text-blue-600 mb-4">
                  ${pkg.price}
                </p>
                <p className="text-gray-600 mb-6">{pkg.description}</p>
                <button
                  onClick={() => handlePackageSelect(pkg)}
                  className={`w-full py-2 px-4 rounded-lg ${
                    selectedPackage?.id === pkg.id
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {selectedPackage?.id === pkg.id ? 'Selected' : 'Select'}
                </button>
              </div>
            </div>
          ))}
        </div>

        {selectedPackage && (
          <div className="mt-8 text-center">
            <button
              onClick={handleCheckout}
              disabled={isLoading}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
            >
              {isLoading ? 'Processing...' : 'Proceed to Checkout'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
} 