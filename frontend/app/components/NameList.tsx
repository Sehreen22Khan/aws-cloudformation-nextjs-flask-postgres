"use client";

type Props = {
  data: Array<{ id: number; name: string }>;
};

export default function NameList({ data }: Props) {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-2">Names in the Database:</h2>
      <ul className="list-disc">
        {data.map((item) => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </div>
  );
}
