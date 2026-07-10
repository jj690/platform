import { useState, useEffect } from 'react'
import styles from './Card.module.css'

const BADGE_LABEL = { active: 'Active', soon: 'Coming Soon', service: 'Service' }
const HEALTH_BASE = (window.__env__ || {}).HEALTHCHECK_URL || '/health'

export function Card({ name, description, href, port, image, color, status, healthCheckId }) {
    const isPlaceholder = status === 'soon'
    const [healthy, setHealthy] = useState(null)

    useEffect(() => {
        if (!healthCheckId) return

        const check = async () => {
            try {
                const res = await fetch(`${HEALTH_BASE}/services/${healthCheckId}`)
                if (!res.ok) { setHealthy(false); return }
                const data = await res.json()
                setHealthy(data[healthCheckId]?.status === 'healthy')
            } catch {
                setHealthy(false)
            }
        }

        check()
        const intervalId = setInterval(check, 30_000)
        return () => clearInterval(intervalId)
    }, [healthCheckId])

    const healthDotClass = healthy === null ? styles.healthUnknown : healthy ? styles.healthUp : styles.healthDown

    const inner = (
        <div className={`${styles.card} ${isPlaceholder ? styles.placeholder : ''}`}>
            <div className={`${styles.banner} ${styles[color]}`}>
                <img src={image} alt={name} className={styles.image} />
            </div>
            <div className={styles.body}>
                <h3 className={styles.title}>{name}</h3>
                <p className={styles.description}>{description}</p>
            </div>
            <div className={styles.footer}>
                <span className={`${styles.badge} ${styles[status]}`}>
                    {BADGE_LABEL[status]}
                </span>
                <div className={styles.footerRight}>
                    {port && <span className={styles.port}>{port}</span>}
                    {healthCheckId && (
                        <span
                            className={`${styles.healthDot} ${healthDotClass}`}
                            title={healthy === null ? 'Checking…' : healthy ? 'Healthy' : 'Unhealthy'}
                        />
                    )}
                </div>
            </div>
        </div>
    )

    if (href && !isPlaceholder) {
        return (
            <a href={href} rel="noreferrer" className={styles.link}>
                {inner}
            </a>
        )
    }
    return inner
}
