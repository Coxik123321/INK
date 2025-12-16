export default function Dashboard() {
  return (
    <div className="mb-6">
      <h2 className="text-xl font-semibold">Общее состояние</h2>
      <ul className="list-disc pl-6">
        <li>Участков с высоким риском: 3</li>
        <li>Критических дефектов: 1</li>
        <li>Рекомендовано ремонтов: 2</li>
      </ul>
    </div>
  );
}
