import { useEffect, useState } from "react";
import { getAllClients } from "../api/requests";
import { Client } from "../api/types";

type ClientListProps = {};

function ClientList({}: ClientListProps): JSX.Element {
  const [clients, setClients] = useState<Client[]>([]);

  useEffect(() => {
    getAllClients().then((cs) => setClients(cs));
  }, []);

  return (
    <div>
      {clients.map((c) => {
        return <p>{c.name}</p>;
      })}
    </div>
  );
}

export default ClientList;
