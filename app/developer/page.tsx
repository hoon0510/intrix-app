import { getServerSession } from "next-auth";
import { redirect } from "next/navigation";
import DeveloperClient from "./DeveloperClient";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";

export default async function DeveloperPage() {
  const session = await getServerSession(authOptions);
  
  if (!session) {
    redirect("/login");
  }
  
  return <DeveloperClient />;
} 