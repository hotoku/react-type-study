import { useEffect, useState } from "react";
import { getAllClients } from "../api/requests";
import { Client, ClientWithDeals } from "../api/types";

type ClientListProps = {};

function ClientList({}: ClientListProps): JSX.Element {
  const [clients, setClients] = useState<ClientWithDeals[]>([]);

  useEffect(() => {
    getAllClients().then((cs) => setClients(cs));
  }, []);

  return (
    <div>
      <ol>
        {clients.map((c) => {
          return <li key={c.id}>{c.name}</li>;
        })}
      </ol>
    </div>
  );
}

export default ClientList;
