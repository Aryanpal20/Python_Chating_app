"use client"
import { useFormik } from 'formik';
import Link from "next/link";
import axios from 'axios';
import { useState } from 'react';

import * as Yup from 'yup';
import { endpoint } from '@/endpoints';
import { useRouter } from 'next/navigation';

const Signup = () => {
    const router = useRouter()
    const [response, setResponse] = useState()
    const [submitError, setSubmitError] = useState()
    const [submitErrorMobilNum, setSubmitErrorMobilNum] = useState()
    const initialValues = {
        first_name: '',
        last_name: '',
        email: '',
        mobile_no: '',
        password: '',
        gender: '',
    };


    const { handleChange, handleSubmit, values, touched, handleBlur, errors } = useFormik({
        initialValues: initialValues,

        validationSchema: Yup.object({
            first_name: Yup.string().min(2).max(20).required('first_name is required'),
            last_name: Yup.string().min(2).max(20).required('last_name is required'),
            email: Yup.string().email('Invalid email address').required('Email is required'),
            password: Yup.string().required('Password is required'),
            mobile_no: Yup.string().required('Mobile No is required'),
            gender: Yup.string().required('Gender is required'),
        }),
        onSubmit: async (values) => {
            const { gender, ...data } = values;
            data.gender = parseInt(gender);
            try {
                const response = await axios.post(endpoint.signup, data);
                if (response.data.message) {
                    router.push("/  ")
                }
                setResponse(response.data.message)
            } catch (error) {
                setSubmitError(error.response.data.email);
                setSubmitErrorMobilNum(error.response.data.mobile_no);
            }
        },
    })






    return (
        <div className="flex justify-center items-center h-screen">

            <form className="bg-white shadow-md rounded px-5 pt-4 pb-5 mb-4 mt-3 w-[35%] " onSubmit={handleSubmit}>
                <h4 className="block text-blue-700  w-full mb-2">{response}</h4>

                <h4 className="block text-gray-700 w-full  mb-2">Registration Form</h4>
                <div className="">
                    <label htmlFor="first_name" className="block text-gray-700 text-xs  ">
                        FirstName
                    </label>
                    <input
                        type="text"
                        name="first_name"
                        id="first_name"

                        className="appearance-none border rounded w-full  px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        onBlur={handleBlur}
                        onChange={handleChange}

                    />
                    {errors.first_name && touched.first_name ? <span className="text-red-600 text-xs">{errors.first_name}</span> : null}
                </div>
                <div className="">
                    <label htmlFor="first_name" className="block text-gray-700 text-xs  ">
                        LastName
                    </label>
                    <input
                        type="text"
                        name="last_name"
                        id="last_name"

                        className="appearance-none border rounded w-full  px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        onBlur={handleBlur}
                        onChange={handleChange}

                    />
                    {errors.last_name && touched.last_name ? <span className="text-red-600 text-xs">{errors.last_name}</span> : null}
                </div>
                <label className="block text-gray-700 text-xs  ">Gender</label>
                <div className="">
                    <label className="inline-flex items-center">
                        <input
                            type="radio"
                            name="gender"
                            value="1"
                            className="form-radio"
                            onChange={handleChange}
                            onBlur={handleBlur}
                            checked={values.gender === '1'}

                        />
                        <span className="ml-2 text-xs">Male</span>
                    </label>
                    <label className="inline-flex items-center ml-6">
                        <input
                            type="radio"
                            name="gender"
                            value="2"
                            className="form-radio"
                            onChange={handleChange}
                            onBlur={handleBlur}
                            checked={values.gender === '2'}
                        />
                        <span className="ml-2 text-xs">Female</span>
                    </label>
                    {errors.gender && touched.gender ? (
                        <span className="text-red-600 text-xs">{errors.gender}</span>
                    ) : null}
                </div>

                <div className="mb-1">
                    <label htmlFor="first_name" className="block text-gray-700 text-xs  ">
                        Mobile No
                    </label>
                    <input
                        type="text"
                        name="mobile_no"
                        id="last_name"
                        className="appearance-none border rounded w-full  px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        onBlur={handleBlur}
                        onChange={handleChange}

                    />
                    {errors.mobile_no && touched.mobile_no ? <span className="text-red-600 text-xs">{errors.mobile_no}</span> : null}
                    <h4 className=" flex text-red-700 w-full text-xs  mb-2">{submitErrorMobilNum}</h4>
                </div>
                <div className="mb-1">
                    <label htmlFor="email" className="block text-gray-700 text-xs  mb-2">
                        Email
                    </label>
                    <input
                        type="email"
                        name="email"
                        id="email"
                        className="appearance-none border rounded w-full  px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        onChange={handleChange}
                        onBlur={handleBlur}

                    />
                    {errors.email && touched.email ? <span className="text-red-600 text-xs">{errors.email}</span> : null}
                    <h4 className=" flex text-red-700 w-full text-xs mb-2">{submitError}</h4>
                </div>
                <div className="mb-2">
                    <label htmlFor="password" className="block text-gray-700 text-xs  mb-2">
                        Password
                    </label>
                    <input
                        type="password"
                        name="password"
                        id="password"
                        className="appearance-none border rounded w-full  px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        onChange={handleChange}
                        onBlur={handleBlur}

                    />
                    {errors.password && touched.password ? <span className="text-red-600 text-xs">{errors.password} </span> : null}
                </div>
                <div className="flex items-center justify-between">
                    <button
                        type="submit"
                        className="bg-blue-500 hover:bg-blue-700 text-white   px-4 rounded focus:outline-none focus:shadow-outline"
                    >
                        Register
                    </button>
                    <Link href='/'>
                        <span className='text-xs'>Already registered</span>

                    </Link>
                </div>
            </form >

        </div >
    );
};

export default Signup;



// import { useFormik } from 'formik';
// import * as Yup from 'yup';

// const SignupForm = () => {
//     const formik = useFormik({
//         initialValues: {
//             firstName: '',
//             lastName: '',
//             email: '',
//         },
//         validationSchema: Yup.object({
//             firstName: Yup.string()
//                 .max(15, 'Must be 15 characters or less')
//                 .required('Required'),
//             lastName: Yup.string()
//                 .max(20, 'Must be 20 characters or less')
//                 .required('Required'),
//             email: Yup.string().email('Invalid email address').required('Required'),
//         }),
//         onSubmit: values => {
//             alert(JSON.stringify(values, null, 2));
//         },
//     });
//     return (
//         <form onSubmit={formik.handleSubmit}>
//             <label htmlFor="firstName">First Name</label>
//             <input
//                 id="firstName"
//                 name="firstName"
//                 type="text"
//                 onChange={formik.handleChange}
//                 onBlur={formik.handleBlur}
//                 value={formik.values.firstName}
//             />
//             {formik.touched.firstName && formik.errors.firstName ? (
//                 <div>{formik.errors.firstName}</div>
//             ) : null}

//             <label htmlFor="lastName">Last Name</label>
//             <input
//                 id="lastName"
//                 name="lastName"
//                 type="text"
//                 onChange={formik.handleChange}
//                 onBlur={formik.handleBlur}
//                 value={formik.values.lastName}
//             />
//             {formik.touched.lastName && formik.errors.lastName ? (
//                 <div>{formik.errors.lastName}</div>
//             ) : null}

//             <label htmlFor="email">Email Address</label>
//             <input
//                 id="email"
//                 name="email"
//                 type="email"
//                 onChange={formik.handleChange}
//                 onBlur={formik.handleBlur}
//                 value={formik.values.email}
//             />
//             {formik.touched.email && formik.errors.email ? (
//                 <div>{formik.errors.email}</div>
//             ) : null}

//             <button type="submit">Submit</button>
//         </form>
//     );
// };
// export default SignupForm;