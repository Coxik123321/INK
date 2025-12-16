export default function Defects() {
  return (
    <div className="mb-6">
      <h2 className="text-xl font-semibold">Дефекты</h2>
      <table className="table-auto border">
        <thead>
          <tr>
            <th>Км</th>
            <th>Тип</th>
            <th>Глубина %</th>
            <th>Риск</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>12.4</td>
            <td>Коррозия</td>
            <td>45</td>
            <td>High</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}
