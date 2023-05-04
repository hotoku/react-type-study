import { useEffect, useState } from "react";
import { getAllClients } from "../api/requests";
import { ClientWithDeals, Deal } from "../api/types";

type DealListItemProps = { deal: Deal };

function DealListItem({ deal }: DealListItemProps): JSX.Element {
  return <li>{deal.name}</li>;
}

type ClientListItemProps = { client: ClientWithDeals };

function ClientListItem({ client }: ClientListItemProps): JSX.Element {
  return (
    <li key={client.id}>
      {client.name}
      <ol>
        {client.deals.map((d) => (
          <DealListItem key={d.id} deal={d} />
        ))}
      </ol>
    </li>
  );
}

function ClientList(): JSX.Element {
  const [clients, setClients] = useState<ClientWithDeals[]>([]);

  useEffect(() => {
    getAllClients().then((cs) => setClients(cs));
  }, []);

  return (
    <div>
      <ol>
        {clients.map((c) => (
          <ClientListItem key={c.id} client={c} />
        ))}
      </ol>
    </div>
  );
}

export default ClientList;
