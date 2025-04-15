import NextAuth from "next-auth/next";
import { authOptions } from "../../../lib/auth_config";

export default NextAuth(authOptions); 