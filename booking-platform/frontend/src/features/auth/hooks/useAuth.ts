/* 

useAuth.ts - Auth Hook 

This is the thin re-export of the useAuth hook from the AuthContext.
Its purpose : follow the feature-based folder structure strictly.
Features should import their hooks from within the feature folder.

Usage in any component:
    import {useAuth} from "../hooks/useAuth"
    const {user,login,logout,isLoading} = useAuth()

What is a custom hook?

A custom hook is a function that starts with "use" and can call other hooks.
It's the React equivalent of a service class that encapsulates logic.
Component's stay "dumb" (UI only) by delegating all logic to hooks.

The hook is the access point and the AuthContext is the registered service.

*/

export { useAuth } from "../../../context/AuthContext";
