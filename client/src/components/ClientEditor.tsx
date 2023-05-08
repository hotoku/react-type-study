import { useState } from "react";
import { createClient } from "../api/requests";
import { Client } from "../api/types";

function ClientEditor(): JSX.Element {
  const [obj, setObj] = useState<Partial<Client>>({});
  return (
    <div>
      <label>
        name
        <input
          style={{ margin: "5px" }}
          value={obj.name ?? ""}
          onChange={(e) => {
            setObj({ ...obj, name: e.target.value });
          }}
        />
      </label>
      <button
        onClick={() => {
          createClient(obj);
        }}
      >
        save
      </button>
    </div>
  );
}

export default ClientEditor;
