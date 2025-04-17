"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2 } from "lucide-react";

interface CreditOption {
  amount: number;
  price: number;
}

const options: CreditOption[] = [
  { amount: 500, price: 499 },      // $4.99
  { amount: 2000, price: 2199 },    // $21.99
  { amount: 10000, price: 8999 },   // $89.99
];

export default function PurchasePage() {
  const [isLoading, setIsLoading] = useState<number | null>(null);

  const handlePurchase = async (amount: number) => {
    setIsLoading(amount);
    try {
      const res = await fetch("/api/payment/create-checkout-session", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ credit_amount: amount }),
      });
      
      if (!res.ok) throw new Error("Failed to create checkout session");
      
      const { url } = await res.json();
      window.location.href = url;
    } catch (error) {
      console.error("Payment error:", error);
      alert("결제 세션 생성 중 오류가 발생했습니다. 다시 시도해주세요.");
    } finally {
      setIsLoading(null);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-10 space-y-8">
      <h1 className="text-2xl font-bold">크레딧 충전</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {options.map((opt) => (
          <Card key={opt.amount} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle className="text-center">{opt.amount} 크레딧</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <p className="text-2xl font-bold mb-4">
                ${(opt.price / 100).toFixed(2)}
              </p>
              <p className="text-sm text-gray-500 mb-4">
                크레딧당 ${(opt.price / opt.amount / 100).toFixed(3)}
              </p>
              <Button
                onClick={() => handlePurchase(opt.amount)}
                disabled={isLoading !== null}
                className="w-full"
              >
                {isLoading === opt.amount ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    처리 중...
                  </>
                ) : (
                  "결제하기"
                )}
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="mt-8 p-4 bg-gray-50 dark:bg-neutral-800 rounded-lg">
        <h2 className="text-lg font-semibold mb-2">결제 안내</h2>
        <ul className="list-disc list-inside space-y-1 text-sm text-gray-600 dark:text-gray-300">
          <li>결제는 Stripe를 통해 안전하게 처리됩니다.</li>
          <li>구매한 크레딧은 즉시 계정에 반영됩니다.</li>
          <li>환불은 구매 후 7일 이내에만 가능합니다.</li>
          <li>문의사항은 support@intrix.com으로 연락주세요.</li>
        </ul>
      </div>
    </div>
  );
} 