import { useEffect, useMemo, useState } from "react";
import { getAllClients } from "../api/requests";
import { Client, ClientWithDeals, Deal } from "../api/types";

function clientOption(client: ClientWithDeals): JSX.Element {
  return (
    <option key={client.id} value={client.id.toString()}>
      {client.name}
    </option>
  );
}

function maybeInt(s: string): number {
  let ret = parseInt(s);
  if (isNaN(ret)) {
    throw new Error(`can not parse as int ${s}`);
  }
  return ret;
}

function DealEditor(): JSX.Element {
  const [clients, setClients] = useState<ClientWithDeals[]>([]);
  const [obj, setObj] = useState<Partial<Deal>>({
    clientId: undefined,
    name: "",
  });

  useEffect(() => {
    getAllClients().then(setClients);
  }, []);

  const options = useMemo(() => {
    return [
      <option key="" value="">
        -
      </option>,
    ].concat(clients.map(clientOption));
  }, [clients]);

  return (
    <div>
      <label>
        client
        <select
          style={{ margin: "10px" }}
          value={obj.clientId ?? ""}
          onChange={(e) => {
            const v = e.target.value;
            setObj({
              ...obj,
              clientId: v === "" ? undefined : maybeInt(v),
            });
          }}
        >
          {options}
        </select>
      </label>
      <label>
        name
        <input
          style={{ margin: "10px" }}
          value={obj.name}
          onChange={(e) => {
            setObj({ ...obj, name: e.target.value });
          }}
        />
      </label>
      <button
        onClick={() => {
          console.log("obj", obj);
        }}
      >
        save
      </button>
    </div>
  );
}

export default DealEditor;
