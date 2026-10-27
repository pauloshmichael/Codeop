"use client";

/**
 * @file components/SWRProvider.jsx
 * @description Global SWR configuration wrapper.
 *
 * Wraps the app with <SWRConfig> so all useSWR() hooks in the app
 * share the same default options without needing to repeat them.
 *
 * Default options set here:
 *   fetcher           — our shared fetcher utility (auto-parses JSON, throws on error)
 *   revalidateOnFocus — false (prevents refetch every time user clicks back to the tab)
 *   errorRetryCount   — 3  (retry failed requests up to 3 times)
 *   dedupingInterval  — 2000ms (deduplicate requests within 2 seconds)
 *
 * Usage: wrap this around your layout's children:
 *   <SWRProvider>{children}</SWRProvider>
 *
 * "use client" is required because SWRConfig uses React context internally.
 */

import { SWRConfig } from "swr";
import { fetcher } from "@/lib/fetcher";

export default function SWRProvider({ children }) {
  return (
    <SWRConfig
      value={{
        fetcher,
        revalidateOnFocus: false,
        errorRetryCount: 3,
        dedupingInterval: 2000,
        onError: (error) => {
          // In production you might log to an error monitoring service here
          if (process.env.NODE_ENV === "development") {
            console.error("[SWR error]", error.message ?? error);
          }
        },
      }}
    >
      {children}
    </SWRConfig>
  );
}
