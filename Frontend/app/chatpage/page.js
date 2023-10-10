"use client"
import { useEffect, useRef, useState } from 'react';
import SideNav from '@/app/componant/nav';
import { BsPersonCircle } from 'react-icons/bs';
import { endpoint } from '@/endpoints';
import axios from 'axios';
import { redirect, useRouter } from 'next/navigation';


const Chats = () => {
    const router = useRouter()
    const [input, setInput] = useState({
        "action": "message",
        "message": "",
        "receiver": ""
    });
    const [chatHistory, setChatHistory] = useState([])
    const [userChat, setUserChat] = useState({})
    const [userLogData, setUserLogData] = useState(null)
    const [isLoading, setIsLoading] = useState(true)
    const socket = useRef(null)

    useEffect(() => {
        const isLogin = JSON.parse(localStorage.getItem('user'))
        console.log(isLogin, "paramnana nandu");
        if (!isLogin) {
            redirect('/')
            setIsLoading(false)
        } else {
            setIsLoading(false)
        }
    }, [])

    useEffect(() => {



        const logid = localStorage.getItem("user") ? JSON.parse(localStorage?.getItem("user")) : ""
        const id = logid.id
        if (userChat.id) {
            try {
                axios.get(`${endpoint.roomId}/?member_1=${id}&member_2=${userChat.id}`).then((res) => {
                    console.log(res, "message");
                    if (res.data.roomId) {

                        axios.get(`${endpoint.messages}/${res.data.id}/messages`).then((res) => {
                            setChatHistory(res.data)
                        })
                        socket.current = new WebSocket(`${endpoint.connection}/${id}/${userChat.id}/`)
                        socket.current.addEventListener("open", (event) => {
                            console.log("socket connected successfully");
                        });

                        const temp = socket.current.addEventListener("message", (event) => {
                            const receivedMessage = JSON.parse(event.data);

                            axios.get(`${endpoint.messages}/${res.data.id}/messages`).then((res) => {
                                setChatHistory(res.data)
                            })

                        });

                        socket.current.addEventListener("close", (event) => {
                            console.log("socket closed ");
                        });

                        return () => {
                            socket.current.close();
                        };
                    }
                })
            } catch (error) {
                console.log(error);
            }
        }
    }, [userChat]);

    const oneToOneConnection = (data) => {
        setUserChat(data)
        setInput({
            ...input,
            receiver: data.id
        })
    }
    const handleSendMessage = () => {
        setInput({
            ...input,
            message: ''
        });
        socket.current.send(JSON.stringify(input));
    };
    const handleInputChange = (e) => {
        setInput({
            ...input,
            message: e.target.value
        });
    }
    const myDivRef = useRef();
    useEffect(() => {
        scrollToBottom();
    }, [chatHistory]);

    const scrollToBottom = () => {
        myDivRef?.current?.scrollTo({
            top: myDivRef?.current.scrollHeight,
        });
    };    

    useEffect(() => {
        const userlogin = JSON.parse(localStorage.getItem('user'))
        console.log(userlogin, "loguserdata");
        setUserLogData(userlogin)
    }, [])
    const logoutHander = (() => {
        localStorage.removeItem("user")
        router.push("/")
    })

    return (
        <>
            {isLoading ? <h1 className='flex  ml-[50%] mx-auto mt-[50%]'>Loading......</h1 > : <>


                <div className='bg-gray-200 w-full h-full'>

                    <div className='flex w-[100%] justify-between  h-[100%]'>
                        <SideNav setUserChat={setUserChat} oneToOneConnection={oneToOneConnection} />
                        <div className='border flex flex-col bg-white overflow-y-auto rounded-md shadow-md w-full mx-2 mt-4 h-[500px] justify-between'>
                            <div className='flex border shadow-lg justify-between p-3 rounded-md  bg-white'>
                                <div className='flex'>
                                    <BsPersonCircle className=' w-8 h-8' />
                                    <p className='mx-1 mt-2 text-blue-400 font-semibold'>{userChat.first_name}</p>
                                    <p className=' mt-2 text-blue-400 font-semibold'>{userChat.last_name}</p>
                                </div>
                                <div className='flex bg-sky-500 p-2 rounded-md text-white'>
                                    <button onClick={logoutHander}>Logout</button>
                                </div>
                            </div>
                            <div className="container h-96 overflow-y-auto px-4 " ref={myDivRef}>
                                {Object.keys(userChat).length ? <div className="mb-4 overflow-y-auto">

                                    {chatHistory.map((chat, index,) => {
                                        // console.log(userid?.first_name && userid?.last_name);

                                        return <>

                                            {chat.userName !== `${userLogData.first_name} ${userLogData.last_name}` ?
                                                <div
                                                    key={index}
                                                    className="flex justify-end flex-col py-2 ext-right "
                                                >
                                                    <div className="ml-2 flex self-end">

                                                    </div>
                                                    <span className="text-gray-700 bg-blue-200 rounded-md p-2 text-right self-end break-all">{chat.message}</span>
                                                </div>
                                                :
                                                <div
                                                    key={index}

                                                    className="flex items-center py-2 w-[50%]"
                                                >

                                                    <div className="ml-2 flex flex-col">

                                                        <span className="text-gray-700 bg-gray-200 p-2 rounded-md">{chat.message
                                                        }</span>
                                                    </div>
                                                </div >


                                            }
                                        </>
                                    })}
                                </div> : <>
                                    <div className='flex justify-center items-center h-64 '>
                                        <h1>no chat selected</h1>
                                    </div>
                                </>}
                            </div>
                            {!!Object.keys(userChat).length && <div className="flex items-center">
                                <input
                                    type="text"
                                    className="border cursor-auto border-gray-300 w-full rounded-l-lg py-2 px-4 flex-1 mr-2 focus:outline-none"
                                    placeholder="Type your message"
                                    value={input.message}
                                    onChange={handleInputChange}
                                />
                                <button
                                    className="bg-blue-500 hover:bg-blue-600  sm:w-[12%] w-10 px-0 text-white py-2 sm:px-4 rounded-r-lg"
                                    onClick={handleSendMessage}
                                >
                                    Send
                                </button>
                            </div>}
                        </div>
                    </div>
                </div >


            </>}

        </>
    );
}

export default Chats



