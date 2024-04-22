import { NextAuthOptions } from 'next-auth'
import CredentialsProvider from "next-auth/providers/credentials";
import DecodeBase64 from '@/components/CipherDecode';
import axios from 'axios';


async function findUserByCredentials(credentials:any){
    // ログイン可能であればユーザidを返し、不可能であればnullを返す
    const login_data = await axios.post(`${process.env.HOST_URL}/user/`,
                                            {user_name:credentials.user});
    console.log(login_data)
    if (!login_data) {
      return null
    } else if(typeof login_data.password === "string"){
        const decodepass = DecodeBase64(login_data.password)
        if (decodepass === credentials.password){
          return login_data
    }else{
        return null
      }
    }
  }

export const authOptions: NextAuthOptions = {
    secret: process.env.NEXTAUTH_SECRET,
  // 認証プロバイダー
  providers: [
    CredentialsProvider({
      // 表示名
      name: "account",
      credentials: {
        user: { label: "Username", type: "text"},
        password: { label: "Password", type: "password" },
      },
      // 認証の関数
      authorize: async (credentials,req) => {
        const user = await findUserByCredentials(credentials)
          if (user) {
            return Promise.resolve(user);
          } else {
            return Promise.resolve(null);
          }
        },
    }),
  ],
  jwt: {
    maxAge: 3 * 24 * 60 * 60,       // 3 days 
  },
}