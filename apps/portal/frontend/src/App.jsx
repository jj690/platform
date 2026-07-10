import { apps, services } from './data/services'
import { Card } from './components/Card'
import './App.css'

export default function App() {
    return (
        <>
            <header>
                <h1>Platform</h1>
                <p>Self-hosted apps &amp; services</p>
            </header>

            <main>
                <section>
                    <h2>Apps</h2>
                    <div className="grid">
                        {apps.map(item => <Card key={item.id} {...item} />)}
                    </div>
                </section>

                <section>
                    <h2>Services</h2>
                    <div className="grid">
                        {services.map(item => <Card key={item.id} {...item} />)}
                    </div>
                </section>
            </main>
        </>
    )
}
