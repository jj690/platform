import appTrackerImg from '../assets/app-tracker.svg'
import pvControlImg from '../assets/pv-control.svg'
import energyDashImg from '../assets/energy-dashboard.svg'
import n8nImg from '../assets/n8n.svg'
import adminerImg from '../assets/adminer.svg'
import traefikImg from '../assets/traefik.svg'

const env = window.__env__ || {}

export const apps = [
    {
        id: 'application-tracker',
        name: 'Application Tracker',
        description: 'Track job applications via email classification and timeline view.',
        href: env.AT_FRONTEND_URL || 'http://localhost/tracker',
        port: '',
        image: appTrackerImg,
        color: 'blue',
        status: 'active',
        healthCheckId: 'tracker_api',
    },
    {
        id: 'pv-control',
        name: 'PV Control',
        description: 'Photovoltaic system monitoring and control.',
        image: pvControlImg,
        color: 'orange',
        status: 'soon',
    },
    {
        id: 'energy-dashboard',
        name: 'Energy Dashboard',
        description: 'Unified energy consumption dashboard.',
        image: energyDashImg,
        color: 'purple',
        status: 'soon',
    },
]

export const services = [
    {
        id: 'n8n',
        name: 'N8N',
        description: 'Workflow automation — processes incoming emails and triggers the classifier.',
        href: env.N8N_URL || 'http://localhost/n8n',
        port: '',
        image: n8nImg,
        color: 'green',
        status: 'service',
        healthCheckId: 'n8n',
    },
    {
        id: 'adminer',
        name: 'Adminer',
        description: 'Database management UI for PostgreSQL.',
        href: env.ADMINER_URL || 'http://localhost/adminer',
        port: '',
        image: adminerImg,
        color: 'gray',
        status: 'service',
        healthCheckId: 'adminer',
    },
    {
        id: 'traefik',
        name: 'Traefik',
        description: 'Reverse proxy and load balancer for routing requests to services.',
        href: env.TRAEFIK_URL || 'http://localhost/traefik',
        port: '',
        image: traefikImg,
        color: 'gray',
        status: 'service',
        healthCheckId: 'traefik',
    }
]
