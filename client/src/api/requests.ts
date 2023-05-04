import { Client } from "./types";

import { validate } from "jsonschema";

export async function getAllClients(): Promise<Client[]> {
  const res = await fetch("/clients");
  const data = await res.json();
  const schema = {
    type: "array",
  };
  validate(data, schema);
  return [];
}
