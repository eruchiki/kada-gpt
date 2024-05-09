"use client";

import React from "react";
import { Button } from "@mui/material";
import { useRouter } from "next/navigation";
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined";


const HomeButton = () => {
  const router = useRouter();
  const Redirect = () => {
    router.push(`/`);
  };
  return (
    <>
      <Button onClick={Redirect}>
        <HomeOutlinedIcon />
        ホーム
      </Button>
    </>
  );
}

export default HomeButton