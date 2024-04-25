'use client';

import Header from '@/src/components/Header';
import Chat from '@/src/components/Chat/Chat';
import { useState } from 'react';
import Axios from 'axios';
import { useSession } from 'next-auth/react';


export default function Page() {
  const threadlist = [{"id":1,"name":"test1"},{"id":2,"name":"test2"}]
  return (
      <>
      <Header threadlist={threadlist}></Header>
      <Chat></Chat>
      </>
    )
}