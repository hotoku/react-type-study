import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createClient } from "../api/requests";
import { Client } from "../api/types";

function ClientEditor(): JSX.Element {
  const [obj, setObj] = useState<Partial<Client>>({});
  const navigate = useNavigate();
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
          createClient(obj).then(() => navigate("/"));
        }}
      >
        save
      </button>
    </div>
  );
}

export default ClientEditor;
