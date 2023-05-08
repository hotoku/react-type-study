import { useEffect, useMemo, useState } from "react";
import { getAllClients } from "../api/requests";
import { Client, ClientWithDeals, Deal } from "../api/types";

function clientOption(client: ClientWithDeals): JSX.Element {
  return (
    <option key={client.id} value={client.id}>
      {client.name}
    </option>
  );
}

function DealEditor(): JSX.Element {
  const [clients, setClients] = useState<ClientWithDeals[]>([]);
  const [obj, setObj] = useState<Partial<Deal>>({ clientId: undefined });

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
        <select style={{ margin: "10px" }} value={obj.clientId ?? ""}>
          {options}
        </select>
      </label>
      <label>
        name
        <input style={{ margin: "10px" }} />
      </label>
    </div>
  );
}

export default DealEditor;
