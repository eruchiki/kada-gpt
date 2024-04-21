import NextAuth from 'next-auth'
import CredentialsProvider from "next-auth/providers/credentials";
import DecodeBase64 from '@/components/CipherDecode';


async function findUserByCredentials(credentials:any){
  // ログイン可能であればユーザidを返し、不可能であればnullを返す
//   const login_data = await APIConnect(`${process.env.HOST_URL}/api/db/UserSearch`,{number:credentials.user})
  console.log(login_data)
  if (!login_data) {
    return null
  } else if(typeof login_data.password === "string"){
      const decodepass = DecodeBase64(login_data.password)
      if (decodepass === credentials.password){
        return {email:login_data.id,name:login_data.student_number}
  }else{
      return null
    }
  }
}

// NextAuth に渡すオプション
export default NextAuth({
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
            // throw new Error(res);
            // console.log(user)
            return Promise.resolve(user);
          } else {
            return Promise.resolve(null);
          }
        },
    }),
  ],
})