'use client';

import Header from '@/components/Header';
import Axios from 'axios';
import { useSession } from 'next-auth/react';
import { useState } from 'react';
import  axios  from 'axios';

export default async function Page() {
  const { data: session, status } = useSession()
  const [ThredList, setThreadList] = useState<Array<any>>([]);
  if (status === 'loading') {
    return <div>Loading...</div>;
  }
  if(!session){
  return (
      <>
      <Header></Header>
      </>
    )
  }else{
    const threadlist = await axios.get(`${process.env.HOST_URL}/user/thread`,
                                        {user_id:session.userid});
    return (
      <>
      <Header></Header>
      </>
    )                                   
  }
}