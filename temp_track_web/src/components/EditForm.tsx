import { FC, useRef, useState } from "react";

import { Form, useForm } from "react-hook-form";

import { EditIcon } from ".";

interface EditFormProps {
  inRange: boolean;
}
interface IFormInput {
  // NOTE: These are named like this to match their JS counterparts
  loc: string;
  min_temp: number;
  max_temp: number;
}

const editFormModalId = "edit-form-modal";

export const EditForm: FC<EditFormProps> = ({ inRange }) => {
  const modalControllerRef = useRef<HTMLInputElement>(null);
  const {
    register,
    control,
    formState: { errors },
  } = useForm<IFormInput>();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  return (
    <>
      <label
        htmlFor={editFormModalId}
        className={`btn btn-outline ${inRange ? "btn-success" : "btn-error"}`}
      >
        <EditIcon /> Edit Range
      </label>

      <input
        ref={modalControllerRef}
        type="checkbox"
        id={editFormModalId}
        className="modal-toggle"
      />
      <div className="modal">
        <div className="modal-box">
          <h3 className="font-bold text-2xl">Edit Range</h3>
          <Form
            action="/api/register"
            encType="application/json"
            control={control}
            className="my-4 mx-2 flex items-center justify-center flex-col"
            onSuccess={({ response }) => {
              setLoading(false);
              console.log(response);
            }}
            onError={async ({ response, error }) => {
              setLoading(false);
              if (response) {
                const data = await response.json();
                setError(data["error"]);
              } else if (error) {
                setError((error as Error).message);
              }
              console.log({ response, error });
            }}
            onSubmit={() => setLoading(true)}
          >
            <div className="form-control w-full max-w-xs">
              <label className="label">
                <span className="label-text">Enter your location</span>
                <span className="label-text-alt">
                  leave empty for autodetect
                </span>
              </label>
              <input
                {...register("loc", { required: false })}
                type="text"
                placeholder="Type here..."
                className="input input-bordered w-full max-w-xs"
              />
            </div>
            <div className="form-control w-full max-w-xs mt-2">
              <label className="label label-text">
                Enter minimum temperature
              </label>
              <input
                {...register("min_temp", {
                  required: {
                    value: true,
                    message: "Please enter a minimum temperature",
                  },
                })}
                type="number"
                placeholder="Type here..."
                className="input input-bordered w-full max-w-xs"
              />
              {errors.min_temp && (
                <label className="label label-text-alt text-error">
                  {errors.min_temp.message}
                </label>
              )}
            </div>
            <div className="form-control w-full max-w-xs mt-2">
              <label className="label label-text">
                Enter maximum temperature
              </label>
              <input
                {...register("max_temp", {
                  required: {
                    value: true,
                    message: "Please enter a maximum temperature",
                  },
                })}
                type="number"
                placeholder="Type here..."
                className="input input-bordered w-full max-w-xs"
              />
              {errors.max_temp && (
                <label className="label label-text-alt text-error">
                  {errors.max_temp.message}
                </label>
              )}
            </div>
            <div className="mt-2 btn-group btn-group-horizontal">
              <button
                type="submit"
                className={`btn ${loading && "btn-disabled"}`}
                disabled={loading}
              >
                {loading && <div className="loading loading-spinner" />} Submit
              </button>
              <button
                className="btn"
                disabled={loading}
                onClick={() => {
                  if (modalControllerRef.current)
                    modalControllerRef.current.checked = false;
                }}
              >
                Cancel
              </button>
            </div>
          </Form>
          {error && (
            <span className="text-error text-lg font-medium">{error}</span>
          )}
        </div>
      </div>
    </>
  );
};
