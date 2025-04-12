'use client';

import React from 'react';

// Mock data
const mockCreditLog = [
  {
    id: 1,
    userId: 'user123',
    amount: 100,
    type: 'charge',
    timestamp: '2024-04-12 10:30:00',
  },
  {
    id: 2,
    userId: 'user456',
    amount: -15,
    type: 'deduction',
    timestamp: '2024-04-12 11:15:00',
  },
  {
    id: 3,
    userId: 'user789',
    amount: -20,
    type: 'refund',
    timestamp: '2024-04-12 12:00:00',
  },
];

const getTypeColor = (type: string) => {
  switch (type) {
    case 'charge':
      return 'text-green-600';
    case 'deduction':
      return 'text-red-600';
    case 'refund':
      return 'text-blue-600';
    default:
      return 'text-gray-600';
  }
};

export default function CreditLogPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">Credit Log</h1>
      
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  User ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Amount
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Timestamp
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {mockCreditLog.map((item) => (
                <tr key={item.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {item.userId}
                  </td>
                  <td className={`px-6 py-4 whitespace-nowrap text-sm ${getTypeColor(item.type)}`}>
                    {item.amount > 0 ? `+${item.amount}` : item.amount}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 capitalize">
                    {item.type}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {item.timestamp}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
} 