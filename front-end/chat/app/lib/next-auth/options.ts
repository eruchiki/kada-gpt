import { NextAuthOptions } from "next-auth";
import { signOut } from "next-auth/react";
import KeycloakProvider from "next-auth/providers/keycloak";
import axios from "axios";
// import CredentialsProvider from "next-auth/providers/credentials";
// import DecodeBase64 from "@/src/components/CipherDecode";
// import GetUser from "../../api/GetUser";

// async function findUserByCredentials(credentials: any) {
//   // ログイン可能であればユーザidを返し、不可能であればnullを返す
//   console.log(credentials);
//   // const login_data = await GetUser(credentials.user)
//   const login_data = { user: "2", group: "1", password: "string" };
//   console.log(login_data);
//   if (!login_data) {
//     return null;
//   } else if (typeof login_data.password === "string") {
//     // const decodepass = DecodeBase64(login_data.password)
//     if (login_data.password === credentials.password) {
//       return { email: login_data.user, name: login_data.group };
//     } else {
//       return null;
//     }
//   }
// }

export const authOptions: NextAuthOptions = {
  secret: process.env.NEXTAUTH_SECRET,
  // 認証プロバイダー
  providers: [
    KeycloakProvider({
      clientId: "frontend_app",
      clientSecret: process.env.KC_KADAGPT_SECRET!,
      issuer: `http://${process.env.START_IP!}:8081/realms/KadaGPT`,
    }),
  ],
  callbacks: {
    async session({ session, token, user }) {
      const url = `${process.env.NEXT_PUBLIC_API_URL}/chat/users`;
      return await axios
        .get(url)
        .then((response) => {
          const user = response.data.find((d: any) =>  d.name === session.user?.name);
          session.user.id = user.id;
          return session;
        })
        .catch((error) => {
          signOut();
          return error;
        });
    },
  },
  session: { strategy: "jwt" },
  jwt: {
    maxAge: 3 * 24 * 60 * 60, // 3 days
  },
};
