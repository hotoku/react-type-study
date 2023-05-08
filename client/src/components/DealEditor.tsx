import { useEffect, useState } from "react";
import { getAllClients } from "../api/requests";
import { Client, ClientWithDeals, Deal } from "../api/types";

function clientOption(client: ClientWithDeals): JSX.Element {
  const ret = [
    <option key="" value="">
      -
    </option>,
  ];
  return (
    <option key={client.id} value={client.id}>
      {client.name}
    </option>
  );
}

function DealEditor(): JSX.Element {
  const [clients, setClients] = useState<ClientWithDeals[]>([]);
  const [obj, setObj] = useState<Partial<Deal>>({});

  useEffect(() => {
    getAllClients().then(setClients);
  }, []);

  return (
    <div>
      <label>
        client
        <select style={{ margin: "10px" }}>{clients.map(clientOption)}</select>
      </label>
      <label>
        name
        <input style={{ margin: "10px" }} />
      </label>
    </div>
  );
}

export default DealEditor;
