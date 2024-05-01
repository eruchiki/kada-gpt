import axios from "axios";


export async function POST(request: Request) {
  const ThreadInfo = await request.json();
  const url = `${process.env.NEXT_PUBLIC_API_URL}/chat/users/${ThreadInfo.create_user_id}/thread`;
  return await axios
    .post(url, ThreadInfo)
    .then((response) => {
      return Response.json(response.data);
    })
    .catch((error) => {
      // 失敗時の処理etc
      return Response.json(error);
    });
}
