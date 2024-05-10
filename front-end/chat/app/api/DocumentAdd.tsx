import axios from "axios";

const DocumentAdd = async (userid:number, collectionid: number, FileData: any, event: any) => {
  event.preventDefault();
  const url = `${process.env.NEXT_PUBLIC_API_URL}/chat/collections/${collectionid}?create_user_id=${userid}`;
  if (FileData) {
    const formData = new FormData();
    for (let i = 0; i < FileData.length; i++) {
      formData.append('files', FileData[i]);
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

export default DocumentAdd;
