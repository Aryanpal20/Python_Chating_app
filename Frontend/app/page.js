"use client"
import { useFormik } from "formik"
import Link from "next/link";
import axios from "axios";
import * as Yup from 'yup';
import { useEffect, useState } from "react";
import { redirect, useRouter } from 'next/navigation'
import { endpoint } from "@/endpoints";
function Home() {

  const router = useRouter()
  const [response, setResponse] = useState()
  const [submitError, setSubmitError] = useState()
  const [isLoading, setIsLoading] = useState(true)
  const initialValues = {
    username: '',
    password: '',
  };



  useEffect(() => {
    const isLogin = JSON.parse(localStorage.getItem('user'))
    if (isLogin) {
      redirect('/chatpage')
      setIsLoading(false)
    } else {
      setIsLoading(false)
    }
  }, [])




  const { handleChange, handleSubmit, values, handleBlur, touched, errors } = useFormik({

    initialValues: initialValues,
    validationSchema: Yup.object({
      username: Yup.string().email('Invalid email address').required('Email is required'),
      password: Yup.string().required('Password is required'),
    }),
    onSubmit: async (values) => {

      try {
        const response = await axios.post(endpoint.login, values);

        setResponse(response.data.message)
        localStorage.setItem('user', JSON.stringify(response.data.data))
        if (response.data.data.access) {
          router.push("/chatpage")
        } else {
          router.push("/")
        }
      } catch (error) {
        setSubmitError(error.response.data.non_field_errors);

      }
    },
  })



  return (
    <>
      {!isLoading ? <form className=" flex flex-col justify-center items-center cursor-default mx-auto mt-[10%] w-[40%]  bg-white shadow-md rounded px-5 pt-4 pb-5 mb-4 " onSubmit={handleSubmit}>
        <h3 className="text-bold">Login to ChatApp </h3>
        <h4 className="text-bold text-blue-600">{response} </h4>
        <h4 className="text-bold text-red-600">{submitError} </h4>

        <div className="mb-1 w-[70%]">
          <label htmlFor="email" className="block text-gray-700 text-xs  mb-2">
            Email
          </label>
          <input
            type="email"
            name="username"
            id="email"
            className=" border rounded w-full  px-3 text-gray-700  "
            onChange={handleChange}
            onBlur={handleBlur}

          />
          {errors.username && touched.username ? <div className="text-red-600 w-full text-xs">{errors.username}</div> : null}
        </div>

        <div className="mb-2 w-[70%]">
          <label htmlFor="password" className="block text-gray-700 text-xs  mb-2">
            Password
          </label>
          <input
            type="password"
            name="password"
            id="password"
            className=" border rounded w-full  px-3 text-gray-700  "
            onChange={handleChange}
            onBlur={handleBlur}

          />
          {errors.password && touched.password ? <div className="text-red-600 text-xs w-full">{errors.password} </div> : null}
        </div>

        <button
          type="submit"
          className="bg-blue-500 hover:bg-blue-700 text-white  cursor-default px-4 rounded focus:outline-none focus:shadow-outline"
        >
          Login
        </button>

        <Link href="/signup">
          <span className="text-xs cursor-pointer">Don't have account Sign up</span>
          <hr className="border" />
        </Link>

      </form> : <>

        <div>loading...</div>

      </>}
    </>
  )
}
export default Home