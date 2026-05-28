'use client';

import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LabelList } from 'recharts';

interface Stats {
  metadata: {
    ref_id: string;
    data_source: string;
    historical_start: string;
    historical_end: string;
    last_pipeline_run: string;
    pipeline_status: string;
    data_freshness: string;
  };
  overview: { total_revenue: number; total_orders: number; growth_rate: number };
  top_products: any[];
  bottom_products: any[];
}

interface MasterData {
  stores: { id: string; name: string }[];
  products: { id: string; name: string; category: string }[];
}

export default function AppDashboard() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [masterData, setMasterData] = useState<MasterData | null>(null);
  const [predictResult, setPredictResult] = useState<any>(null);
  const [rainProb, setRainProb] = useState<number>(0);
  const [loading, setLoading] = useState(false);
  
  const [form, setForm] = useState({
    store_id: '',
    product_id: '',
    target_date: new Date().toISOString().split('T')[0],
    is_holiday: false,
    has_promotion: false
  });

  useEffect(() => {
    Promise.all([
      fetch('https://test-project.onrender.com/api/stats').then(res => res.json()),
      fetch('https://test-project.onrender.com/api/master-data').then(res => res.json())
    ]).then(([statsData, master]) => {
      setStats(statsData);
      setMasterData(master);
      setForm(prev => ({
        ...prev,
        store_id: master.stores[0].id,
        product_id: master.products[0].id
      }));
    }).catch(console.error);
  }, []);

  useEffect(() => {
    if (form.store_id && form.target_date) {
      fetch(`https://test-project.onrender.com/api/weather?target_date=${form.target_date}&store_id=${form.store_id}`)
        .then(res => res.json())
        .then(data => setRainProb(data.rain_probability))
        .catch(console.error);
    }
  }, [form.store_id, form.target_date]);

  const handlePredict = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch('https://test-project.onrender.com/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      });
      const data = await res.json();
      setTimeout(() => {
        setPredictResult(data);
        setLoading(false);
      }, 400); 
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  if (!stats || !masterData) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="text-xl font-bold text-slate-500 animate-pulse">Initializing Data Operations...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-100 p-6 md:p-8 font-sans text-slate-900 flex flex-col justify-between">
      <div className="max-w-7xl mx-auto space-y-8 w-full flex-grow">
        
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-slate-200 pb-6">
          <div>
            <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">Retail Inventory Operations</h1>
            <p className="text-slate-500 font-medium mt-1">Data-Driven Demand Forecasting & Analytics</p>
          </div>
          
          <div className="bg-slate-200/60 p-4 rounded-xl text-xs space-y-1 text-slate-700 border border-slate-300 max-w-md">
            <div><span className="font-bold">แหล่งข้อมูล:</span> {stats.metadata.data_source}</div>
            <div><span className="font-bold">ช่วงข้อมูลสถิติ:</span> {stats.metadata.historical_start} ถึง {stats.metadata.historical_end}</div>
            <div><span className="font-bold">ประมวลผลล่าสุด:</span> {stats.metadata.last_pipeline_run} ({stats.metadata.data_freshness})</div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-center gap-4">
            <div className="p-3 bg-emerald-100 text-emerald-700 rounded-lg text-xl">💰</div>
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-slate-500">ยอดขายรวม</p>
              <h3 className="text-2xl font-black text-slate-800">฿{stats.overview.total_revenue.toLocaleString()}</h3>
            </div>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-center gap-4">
            <div className="p-3 bg-blue-100 text-blue-700 rounded-lg text-xl">📦</div>
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-slate-500">จำนวนออเดอร์</p>
              <h3 className="text-2xl font-black text-slate-800">{stats.overview.total_orders.toLocaleString()}</h3>
            </div>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-center gap-4">
            <div className="p-3 bg-indigo-100 text-indigo-700 rounded-lg text-xl">📈</div>
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-slate-500">อัตราเติบโต</p>
              <h3 className="text-2xl font-black text-slate-800">+{stats.overview.growth_rate}%</h3>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500 mb-6">สินค้าความต้องการสูง (Top 3)</h3>
            <div className="h-[250px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={stats.top_products} layout="vertical" margin={{ top: 0, right: 60, left: 0, bottom: 0 }}>
                  <XAxis type="number" hide />
                  <YAxis dataKey="name" type="category" axisLine={false} tickLine={false} tick={{ fontWeight: 600, fontSize: 13 }} width={140} />
                  <Tooltip cursor={{ fill: '#f1f5f9' }} contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0' }} />
                  <Bar dataKey="qty" fill="#3b82f6" radius={[0, 4, 4, 0]} barSize={24}>
                    <LabelList dataKey="qty" position="right" formatter={(val: number) => `${val.toLocaleString()} ชิ้น`} style={{ fontWeight: 700, fontSize: '13px', fill: '#1e293b' }} />
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500 mb-6">สินค้าหมุนเวียนต่ำ (Low Sales)</h3>
            <div className="h-[250px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={stats.bottom_products} layout="vertical" margin={{ top: 0, right: 60, left: 0, bottom: 0 }}>
                  <XAxis type="number" hide />
                  <YAxis dataKey="name" type="category" axisLine={false} tickLine={false} tick={{ fontWeight: 600, fontSize: 13 }} width={140} />
                  <Tooltip cursor={{ fill: '#f1f5f9' }} contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0' }} />
                  <Bar dataKey="qty" fill="#ef4444" radius={[0, 4, 4, 0]} barSize={24}>
                    <LabelList dataKey="qty" position="right" formatter={(val: number) => `${val.toLocaleString()} ชิ้น`} style={{ fontWeight: 700, fontSize: '13px', fill: '#1e293b' }} />
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        <div className="bg-white p-8 rounded-xl shadow-sm border border-slate-200">
          <div className="mb-8 border-b border-slate-100 pb-4">
            <h2 className="text-xl font-bold text-slate-900">Demand Forecasting Engine</h2>
            <p className="text-sm text-slate-500">ระบุพารามิเตอร์เพื่อจำลองความต้องการสินค้า</p>
          </div>
          
          <div className="grid lg:grid-cols-12 gap-10 items-start">
            
            <form onSubmit={handlePredict} className="lg:col-span-5 space-y-5">
              <div className="space-y-1.5">
                <label className="text-xs font-bold uppercase tracking-wider text-slate-500">วันที่ต้องการพยากรณ์</label>
                <input 
                  type="date" 
                  value={form.target_date}
                  onChange={(e) => setForm(prev => ({ ...prev, target_date: e.target.value }))}
                  className="w-full bg-slate-50 border border-slate-200 text-slate-900 font-semibold rounded-lg px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-bold uppercase tracking-wider text-slate-500">สาขา</label>
                <select 
                  value={form.store_id}
                  onChange={(e) => setForm(prev => ({ ...prev, store_id: e.target.value }))}
                  className="w-full bg-slate-50 border border-slate-200 text-slate-900 font-semibold rounded-lg px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
                >
                  {masterData.stores.map(store => (
                    <option key={store.id} value={store.id}>{store.name}</option>
                  ))}
                </select>
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-bold uppercase tracking-wider text-slate-500">SKU สินค้า</label>
                <select 
                  value={form.product_id}
                  onChange={(e) => setForm(prev => ({ ...prev, product_id: e.target.value }))}
                  className="w-full bg-slate-50 border border-slate-200 text-slate-900 font-semibold rounded-lg px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
                >
                  {masterData.products.map(product => (
                    <option key={product.id} value={product.id}>
                      [{product.category}] {product.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-bold uppercase tracking-wider text-slate-500">พยากรณ์สภาพอากาศ (ระบบดึงข้อมูลอัตโนมัติ)</label>
                <div className="w-full bg-blue-50 border border-blue-200 text-blue-900 font-semibold rounded-lg px-4 py-3 flex justify-between items-center shadow-sm">
                  <div className="flex items-center gap-2">
                    <span className="text-xl">{rainProb >= 70 ? '⛈️' : rainProb >= 40 ? '🌥️' : '☀️'}</span>
                    <span className="text-sm">โอกาสเกิดฝนตก (PoP)</span>
                  </div>
                  <span className="text-lg font-black">{rainProb}%</span>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setForm(prev => ({ ...prev, is_holiday: !prev.is_holiday }))}
                  className={`p-3 rounded-lg border text-center transition-all flex items-center justify-center gap-2 ${
                    form.is_holiday ? 'bg-slate-900 border-slate-900 text-white' : 'bg-white border-slate-200 text-slate-600'
                  }`}
                >
                  <span className="text-sm font-bold">ตรงกับเทศกาล</span>
                </button>

                <button
                  type="button"
                  onClick={() => setForm(prev => ({ ...prev, has_promotion: !prev.has_promotion }))}
                  className={`p-3 rounded-lg border text-center transition-all flex items-center justify-center gap-2 ${
                    form.has_promotion ? 'bg-slate-900 border-slate-900 text-white' : 'bg-white border-slate-200 text-slate-600'
                  }`}
                >
                  <span className="text-sm font-bold">กำลังจัดโปรฯ</span>
                </button>
              </div>

              <button type="submit" disabled={loading} className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3.5 rounded-lg transition-all mt-4 disabled:opacity-50">
                {loading ? 'Processing...' : 'Run Analysis'}
              </button>
            </form>

            <div className="lg:col-span-7 flex flex-col gap-6 lg:pl-6 lg:border-l border-slate-100">
              {predictResult ? (
                <>
                  <div className="bg-slate-50 p-8 rounded-xl border border-slate-200 text-center">
                    <p className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">เป้าหมายสต็อกที่แนะนำ</p>
                    <div className="flex justify-center items-end gap-2 text-slate-900 mb-4">
                      <span className="text-7xl font-black tracking-tight">{predictResult.predicted_qty}</span>
                      <span className="text-xl font-bold mb-2 text-slate-500">ชิ้น</span>
                    </div>
                    <span className={`inline-flex items-center px-4 py-1.5 rounded-md text-sm font-bold ${
                      predictResult.status.includes('🔥') ? 'bg-red-100 text-red-700' : 
                      predictResult.status.includes('✅') ? 'bg-emerald-100 text-emerald-700' : 
                      'bg-slate-200 text-slate-700'
                    }`}>
                      {predictResult.status}
                    </span>
                  </div>

                  <div>
                    <p className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">คำแนะนำการจัดวาง (Market Basket)</p>
                    <div className="space-y-3">
                      {predictResult.recommendations.map((item: any, idx: number) => (
                        <div key={idx} className="bg-white p-4 rounded-xl border border-slate-200 flex justify-between items-center">
                          <p className="font-bold text-slate-800 text-sm">{item.name}</p>
                          <div className="text-right">
                            <p className="font-black text-blue-600">{item.est_sales} ชิ้น</p>
                            <p className="text-[11px] font-bold text-slate-500">{item.trend}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </>
              ) : (
                <div className="h-full min-h-[300px] flex flex-col items-center justify-center text-slate-400 bg-slate-50 rounded-xl border border-dashed border-slate-300">
                  <p className="font-medium text-sm">Waiting for parameters...</p>
                </div>
              )}
            </div>

          </div>
        </div>

      </div>

      <div className="max-w-6xl mx-auto w-full mt-8 pt-4 border-t border-slate-200 flex flex-col md:flex-row justify-between text-[11px] text-slate-500 gap-2">
        <div><span className="font-bold">รหัสอ้างอิงข้อมูล:</span> {stats.metadata.ref_id} | <span className="font-bold">ระบบต้นทาง:</span> {stats.metadata.data_source}</div>
        <div><span className="font-bold">ขอบเขตข้อมูลสถิติครอบคลุม:</span> วันที่ {stats.metadata.historical_start} ถึง วันที่ {stats.metadata.historical_end} (ข้อมูลสมบูรณ์ล่าสุดก่อนวันปัจจุบัน)</div>
      </div>
    </div>
  );
}