'use client';

import React, { useState } from 'react';

// Mock data
const mockRefundRequests = [
  {
    id: 1,
    userId: 'user123',
    amount: 50,
    reason: 'Unsatisfactory analysis results',
    status: 'pending',
    timestamp: '2024-04-12 10:30:00',
  },
  {
    id: 2,
    userId: 'user456',
    amount: 30,
    reason: 'Technical issues during analysis',
    status: 'approved',
    timestamp: '2024-04-12 11:15:00',
  },
  {
    id: 3,
    userId: 'user789',
    amount: 20,
    reason: 'Duplicate charge',
    status: 'rejected',
    timestamp: '2024-04-12 12:00:00',
  },
];

const getStatusColor = (status: string) => {
  switch (status) {
    case 'pending':
      return 'bg-yellow-100 text-yellow-800';
    case 'approved':
      return 'bg-green-100 text-green-800';
    case 'rejected':
      return 'bg-red-100 text-red-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

export default function RefundPage() {
  const [requests, setRequests] = useState(mockRefundRequests);

  const handleStatusChange = (id: number, newStatus: string) => {
    setRequests(requests.map(request => 
      request.id === id ? { ...request, status: newStatus } : request
    ));
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">Refund Requests</h1>
      
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
                  Reason
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Timestamp
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {requests.map((item) => (
                <tr key={item.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {item.userId}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {item.amount}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    {item.reason}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(item.status)}`}>
                      {item.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {item.timestamp}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {item.status === 'pending' && (
                      <div className="space-x-2">
                        <button
                          onClick={() => handleStatusChange(item.id, 'approved')}
                          className="text-green-600 hover:text-green-900"
                        >
                          Approve
                        </button>
                        <button
                          onClick={() => handleStatusChange(item.id, 'rejected')}
                          className="text-red-600 hover:text-red-900"
                        >
                          Reject
                        </button>
                      </div>
                    )}
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