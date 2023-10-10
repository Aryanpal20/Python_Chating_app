"use client"
import { redirect, useRouter } from 'next/navigation';
import React, { useLayoutEffect } from 'react'

const Loading = () => {

    useLayoutEffect(() => {
        const useraccess = localStorage.getItem("user") ? JSON.parse(localStorage?.getItem("user")) : null
        const access = useraccess?.access
        if (!access) {
            redirect("/")
        }
    })

    return (
        <div className='flex  ml-[50%] mt-[50%]'>Loading...</div>
    )
}

export default Loading