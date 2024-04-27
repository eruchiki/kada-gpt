import axios from "axios";

const GetThreadList = async (userid: string) => {
  const url = `http://localhost:8080/chat/users/${userid}/thread`;
    return await axios.get(url).then(response => {
      return response.data
    }).catch(error => {
        // 失敗時の処理etc
        return error
    })
}

export default GetThreadList;
