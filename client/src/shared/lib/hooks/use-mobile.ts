import { useSyncExternalStore } from "react"

const MOBILE_BREAKPOINT = 768
const MOBILE_QUERY = `(max-width: ${MOBILE_BREAKPOINT - 1}px)`

const subscribe = (onChange: () => void) => {
  const mql = window.matchMedia(MOBILE_QUERY)
  mql.addEventListener("change", onChange)
  return () => mql.removeEventListener("change", onChange)
}

const getSnapshot = () => window.matchMedia(MOBILE_QUERY).matches

// useSyncExternalStore instead of useState + useEffect: a media query is an
// external source, and the very first render gets the right value without flicker.
export function useIsMobile() {
  return useSyncExternalStore(subscribe, getSnapshot, () => false)
}
