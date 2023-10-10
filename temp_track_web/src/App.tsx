import {
  EditForm,
  ErrorIcon,
  LoadingIndicator,
  RefreshIcon,
} from "./components";
import { useGetStatusQuery } from "./utils";

export default function App() {
  const { data, error, isLoading, isError, refetch } =
    useGetStatusQuery("mumbai");
  if (isLoading)
    return (
      <>
        <LoadingIndicator />
        <div className={`grid place-items-center h-screen bg-blue-100`}>
          <div className="text-center max-w-4xl">
            <div className="my-8 py-5 border-b-2 border-slate-500 w-fit mx-auto">
              <h1 className="text-3xl md:text-5xl lg:text-7xl text-slate-700 font-bold">
                Temp Track
              </h1>
            </div>
          </div>
        </div>
      </>
    );

  if (isError)
    return (
      <div className={`grid place-items-center h-screen bg-blue-100`}>
        <div className="text-center max-w-4xl">
          <div className="my-8 py-5 border-b-2 border-slate-500 w-fit mx-auto">
            <h1 className="text-3xl md:text-5xl lg:text-7xl text-slate-700 font-bold">
              Temp Track
            </h1>
          </div>
          <div className="text-red-500">
            <ErrorIcon className="h-12 w-12" /> An error occurred!
            <pre>{JSON.stringify(error)}</pre>
          </div>
        </div>
      </div>
    );

  if (data)
    return (
      <div
        className={`grid place-items-center h-screen ${
          data["within_range"] ? "bg-green-200" : "bg-red-200"
        } transition-colors`}
      >
        <div className="text-center max-w-4xl">
          <div className="my-8 py-5 border-b-2 border-slate-500 w-fit mx-auto">
            <h1 className="text-3xl md:text-5xl lg:text-7xl text-slate-700 font-bold">
              Temp Track
            </h1>
          </div>
          <h3 className="text-slate-700 text-xl md:text-3xl lg:text-5xl">
            The current temperature{" "}
            <span className="text-blue-500 font-medium">
              ({data["curr_temp"]})
            </span>{" "}
            is{" "}
            {data["within_range"] ? (
              <span className="text-green-800 font-semibold">within</span>
            ) : (
              <span className="text-red-800 font-semibold">outside</span>
            )}{" "}
            the specified range{" "}
            <span className="text-blue-500 font-medium">
              ({data["min_temp"]}-{data["max_temp"]})
            </span>
            !
          </h3>
          <h4 className="mt-3 text-slate-600 text-lg">
            Current location: <b>{data["loc_name"]}</b>
          </h4>
          <div className="m-5 btn-group btn-group-horizontal">
            <EditForm inRange={data["within_range"]} />
            <button
              className={`btn btn-outline ${
                data["within_range"] ? "btn-success" : "btn-error"
              }`}
              onClick={refetch}
            >
              <RefreshIcon /> Refresh
            </button>
          </div>
        </div>
      </div>
    );
}
