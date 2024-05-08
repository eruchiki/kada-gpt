import axios from "axios";

export const POST = async (request: Request) => {
  const Data = await request.json();
  const url = `${process.env.NEXT_PUBLIC_API_URL}/chat/collections/${Data.collectionid}?create_user_id=${Data.userid}`;
  if (Data.FileData) {
    const formData = new FormData();
    for (let i = 0; i < Data.FileData.length; i++) {
      formData.append("files", Data.FileData[i]);
    }
    return await axios
      .post(url, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        return response.data;
      })
      .catch((error) => {
        // 失敗時の処理etc
        return error;
      });
  }
};


